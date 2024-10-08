using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using ApiBotDiscord.Domain.Models;
using ApiBotDiscord.Infraestrutura;
using ApiBotDiscord.Domain.viewmodels;
using Microsoft.AspNetCore.Authorization;
using ApiBotDiscord.Domain.Dto;

namespace ApiBotDiscord.Controllers
{
    [Authorize]
    [Route("api/[controller]")]
    [ApiController]
    public class PersonagemsController : ControllerBase
    {
        private readonly PersonagemContext _context;
        private readonly FranquiaContext _contextFranquia;

        public PersonagemsController(PersonagemContext context, FranquiaContext contextFranquia)
        {
            _context = context;
            _contextFranquia = contextFranquia;
        }

        // GET: api/Personagems
        [HttpGet]
        [AllowAnonymous]
        public async Task<ActionResult<IEnumerable<Personagem>>> GetPersonagemSet()
        {
            return await _context.PersonagemSet.ToListAsync();
        }
        // GET: api/Personagems/5
        [HttpGet("{id}")]
        [AllowAnonymous]
        public async Task<ActionResult<Personagem>> GetPersonagem(int id)
        {
            var personagem = await _context.PersonagemSet.FindAsync(id);

            if (personagem == null)
            {
                return NotFound();
            }

            return personagem;
        }
        [HttpGet("franquia/{id_franquia}")] // Rota que aceita um id de franquia
        [AllowAnonymous]
        public async Task<ActionResult<IEnumerable<Personagem>>> GetPersonagensByFranquia(int id_franquia, int pageNumber = 0, int pageQuantity = 10)
        {
            try
            {
                // Validar valores de paginação
                if (pageNumber < 0)
            {
                return BadRequest(new { mensagem = "O número da página não pode ser negativo." });
            }

            if (pageQuantity <= 0)
            {
                return BadRequest(new { mensagem = "A quantidade de itens por página deve ser maior que zero." });
            }
            // Filtra os personagens que pertencem à franquia especificada
            var personagens = await _context.PersonagemSet
                .Where(p => p.Id_Franquia == id_franquia) // Supondo que IdFranquia é a propriedade que relaciona o personagem à franquia
                .Skip(pageNumber * pageQuantity) // Pula os registros das páginas anteriores
                .Take(pageQuantity) // Pega a quantidade de registros solicitados
                .ToListAsync();

            if (personagens == null || !personagens.Any())
            {
                return NotFound(); // Retorna 404 se não encontrar personagens
            }

            return Ok(personagens); // Retorna a lista de personagens encontrados
            }
            catch (Exception ex)
            {
                // Logar o erro (opcional: você pode logar o erro em um sistema de log)
                Console.WriteLine($"Erro ao obter as Personagem paginadas: {ex.Message}");

                // Retornar status 500 com a mensagem de erro
                return StatusCode(500, new { mensagem = "Ocorreu um erro ao obter as franquias paginadas.", erro = ex.Message });
            }
        }
        [AllowAnonymous]
        [HttpGet("Pag")] // Retorna todas as franquias com paginação
        public async Task<ActionResult<IEnumerable<Personagem>>> GetPagPersonagemSet(int pageNumber = 0, int pageQuantity = 10)
        {
            try
            {
                // Validar valores de paginação
                if (pageNumber < 0)
                {
                    return BadRequest(new { mensagem = "O número da página não pode ser negativo." });
                }

                if (pageQuantity <= 0)
                {
                    return BadRequest(new { mensagem = "A quantidade de itens por página deve ser maior que zero." });
                }

                // Calcular total de registros
                var totalRecords = await _context.PersonagemSet.CountAsync();

                // Obter registros paginados
                var franquiasPaginadas = await _context.PersonagemSet
                    .Skip(pageNumber * pageQuantity) // Pula os registros das páginas anteriores
                    .Take(pageQuantity) // Pega a quantidade de registros solicitados
                    .ToListAsync();

                // Retornar dados de paginação e as franquias
                return Ok(new
                {
                    PageNumber = pageNumber,
                    PageQuantity = pageQuantity,
                    TotalRecords = totalRecords,
                    TotalPages = (int)Math.Ceiling((double)totalRecords / pageQuantity), // Total de páginas
                    Franquias = franquiasPaginadas
                });
            }
            catch (Exception ex)
            {
                // Logar o erro (opcional: você pode logar o erro em um sistema de log)
                Console.WriteLine($"Erro ao obter as Personagem paginadas: {ex.Message}");

                // Retornar status 500 com a mensagem de erro
                return StatusCode(500, new { mensagem = "Ocorreu um erro ao obter as franquias paginadas.", erro = ex.Message });
            }
        }

        // PUT: api/Personagems/5
        [HttpPut("{id}")]
        public async Task<IActionResult> PutPersonagem(int id, AtualizarPersonagemDTO personagem)
        {

            try
            {

            // Verifica se o personagem existe antes de tentar atualizar
            var existingPersonagem = await _context.PersonagemSet.FindAsync(id);
            if (existingPersonagem == null)
            {
                return NotFound();
            }
            // Verificar se o gênero fornecido é válido
            if (!Enum.TryParse(personagem.Gender, true, out GenderEnum genderEnum))
            {
                return BadRequest(new { mensagem = "Gênero inválido. Por favor, forneça um valor válido: Feminino, Masculino, Não-Binário, Fluido, Outros." });
            }

            // Criar um novo personagem e associar à franquia existente
            var AtualizarPersonagem = new Personagem
            {
                Name = personagem.Name,
                Gender = genderEnum, // Utilizar o valor da enumeração
                CaminhoArquivo = existingPersonagem.CaminhoArquivo,
            };
                _context.Entry(AtualizarPersonagem).State = EntityState.Modified;
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!PersonagemExists(id))
                {
                    return NotFound();
                }
                else
                {
                    throw;
                }
            }

            return NoContent();
        }


        // POST: api/Personagems
        // To protect from overposting attacks, see https://go.microsoft.com/fwlink/?linkid=2123754
        [HttpPost]
        public async Task<ActionResult<Personagem>> PostPersonagem([FromForm] PersonagemViewModel personagemViewModel)
        {
            try
            {
                // Verificar se a franquia existe pelo nome
                var franquia = await _contextFranquia.FranquiaSet
                    .FirstOrDefaultAsync(f => f.Name == personagemViewModel.Name_Franquia);

                if (franquia == null)
                {
                    return BadRequest(new { mensagem = "Franquia não encontrada. Por favor, verifique o nome da franquia." });
                }

                // Verificar se o arquivo enviado é uma imagem
                var permittedExtensions = new[] { ".jpg", ".jpeg", ".png", ".gif" };
                var ext = Path.GetExtension(personagemViewModel.ArquivoPersonagem.FileName).ToLowerInvariant();
                if (!permittedExtensions.Contains(ext))
                {
                    return BadRequest(new { mensagem = "Arquivo inválido. Apenas imagens (.jpg, .jpeg, .png, .gif) são permitidas." });
                }

                // Verificar se o gênero fornecido é válido
                if (!Enum.TryParse(personagemViewModel.Gender, true, out GenderEnum genderEnum))
                {
                    return BadRequest(new { mensagem = "Gênero inválido. Por favor, forneça um valor válido: Feminino, Masculino, Não-Binário, Fluido, Outros." });
                }

                // Criar o caminho para o arquivo
                var fileNameWithoutExtension = Path.GetFileNameWithoutExtension(personagemViewModel.ArquivoPersonagem.FileName);
                var fileName = fileNameWithoutExtension;
                var filePath = Path.Combine("Storage/Personagens", personagemViewModel.ArquivoPersonagem.FileName);

                // Verifica se o arquivo já existe e, se sim, cria um novo nome
                int count = 1;
                while (System.IO.File.Exists(filePath))
                {
                    fileName = $"{fileNameWithoutExtension}_{count++}{ext}";
                    filePath = Path.Combine("Storage/Personagens", fileName);
                }

                // Salvar o arquivo no sistema de arquivos
                using (Stream fileStream = new FileStream(filePath, FileMode.Create))
                {
                    await personagemViewModel.ArquivoPersonagem.CopyToAsync(fileStream);
                }

                // Criar um novo personagem e associar à franquia existente
                var novoPersonagem = new Personagem
                {
                    Name = personagemViewModel.Name,
                    Gender = genderEnum, // Utilizar o valor da enumeração
                    CaminhoArquivo = filePath,
                    Id_Franquia = franquia.Id, // Associar à franquia encontrada
                };

                // Adicionar o personagem ao contexto
                _context.PersonagemSet.Add(novoPersonagem);
                await _context.SaveChangesAsync();

                return Ok(novoPersonagem);
            }
            catch (Exception ex)
            {
                // Logar o erro e retornar um status de erro apropriado
                return StatusCode(500, new { mensagem = "Ocorreu um erro ao cadastrar o personagem.", erro = ex.Message });
            }
        }

        [AllowAnonymous]
        [HttpGet("DownloadPersonagemByName")]
        public async Task<IActionResult> DownloadPersonagemByName(string nome, string? franquia = null)
        {
            try
            {
                // Valida se o nome foi fornecido
                if (string.IsNullOrWhiteSpace(nome))
                {
                    return BadRequest(new { mensagem = "O nome do personagem é obrigatório." });
                }

                Personagem personagem;

                // Verifica se a franquia foi fornecida
                if (!string.IsNullOrWhiteSpace(franquia))
                {
                    // Busca a franquia com base no nome
                    var franquiaEntity = await _contextFranquia.FranquiaSet.FirstOrDefaultAsync(f => f.Name == franquia);

                    if (franquiaEntity == null)
                    {
                        return NotFound(new { mensagem = "Franquia não encontrada." });
                    }

                    // Busca o personagem com base no nome e na franquia fornecida
                    personagem = await _context.PersonagemSet
                        .FirstOrDefaultAsync(p => p.Name == nome && p.Id_Franquia == franquiaEntity.Id);

                    if (personagem == null)
                    {
                        return NotFound(new { mensagem = "Personagem não encontrado para o nome e franquia especificados." });
                    }
                }
                else
                {
                    // Busca o personagem apenas com base no nome
                    var personagens = await _context.PersonagemSet
                        .Where(p => p.Name == nome)
                        .ToListAsync();

                    if (!personagens.Any())
                    {
                        return NotFound(new { mensagem = "Nenhum personagem encontrado com esse nome." });
                    }

                    // Verifica se existem personagens com o mesmo nome, mas de franquias diferentes
                    if (personagens.Count > 1)
                    {
                        return BadRequest(new
                        {
                            mensagem = "Existem vários personagens com o mesmo nome. Por favor, especifique a franquia para refinar a busca.",
                            personagens = personagens.Select(p => new { p.Name }).ToList()
                        });
                    }

                    personagem = personagens.First(); // Retorna o único personagem encontrado
                }

                // Verifica se o arquivo existe no caminho fornecido
                var filePath = personagem.CaminhoArquivo;
                if (!System.IO.File.Exists(filePath))
                {
                    return NotFound(new { mensagem = "Arquivo não encontrado no servidor." });
                }

                // Lê o arquivo em bytes
                byte[] fileBytes = System.IO.File.ReadAllBytes(filePath);

                // Determina o tipo MIME do arquivo com base na extensão
                var mimeType = GetMimeType(filePath);

                // Retorna o arquivo para download
                return File(fileBytes, mimeType, Path.GetFileName(filePath));
            }
            catch (Exception ex)
            {
                return StatusCode(500, new { mensagem = "Ocorreu um erro ao baixar a imagem do personagem.", erro = ex.Message });
            }
        }

        // Método auxiliar para determinar o tipo MIME com base na extensão do arquivo
        private string GetMimeType(string filePath)
        {
            var ext = Path.GetExtension(filePath).ToLowerInvariant();
            return ext switch
            {
                ".jpg" or ".jpeg" => "image/jpeg",
                ".png" => "image/png",
                ".gif" => "image/gif",
                _ => "application/octet-stream", // Default para arquivos não reconhecidos
            };
        }


        // DELETE: api/Personagems/5
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeletePersonagem(int id)
        {
            var personagem = await _context.PersonagemSet.FindAsync(id);
            if (personagem == null)
            {
                return NotFound();
            }

            _context.PersonagemSet.Remove(personagem);
            await _context.SaveChangesAsync();

            return NoContent();
        }

        private bool PersonagemExists(int id)
        {
            return _context.PersonagemSet.Any(e => e.Id == id);
        }
    }
}

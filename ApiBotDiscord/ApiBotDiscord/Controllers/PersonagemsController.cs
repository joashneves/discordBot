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

namespace ApiBotDiscord.Controllers
{
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
        public async Task<ActionResult<IEnumerable<Personagem>>> GetPersonagemSet()
        {
            return await _context.PersonagemSet.ToListAsync();
        }

        // GET: api/Personagems/5
        [HttpGet("{id}")]
        public async Task<ActionResult<Personagem>> GetPersonagem(int id)
        {
            var personagem = await _context.PersonagemSet.FindAsync(id);

            if (personagem == null)
            {
                return NotFound();
            }

            return personagem;
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
        // To protect from overposting attacks, see https://go.microsoft.com/fwlink/?linkid=2123754
        [HttpPut("{id}")]
        public async Task<IActionResult> PutPersonagem(int id, Personagem personagem)
        {
            if (id != personagem.Id)
            {
                return BadRequest();
            }

            _context.Entry(personagem).State = EntityState.Modified;

            try
            {
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
                var filePath = Path.Combine("Storage/Personagens", personagemViewModel.ArquivoPersonagem.FileName);

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

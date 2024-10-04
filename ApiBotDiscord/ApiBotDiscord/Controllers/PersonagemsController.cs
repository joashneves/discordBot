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

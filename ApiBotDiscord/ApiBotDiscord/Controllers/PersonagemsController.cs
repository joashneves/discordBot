using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using ApiBotDiscord.Domain.Models;
using ApiBotDiscord.Infraestrutura;

namespace ApiBotDiscord.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class PersonagemsController : ControllerBase
    {
        private readonly PersonagemContext _context;

        public PersonagemsController(PersonagemContext context)
        {
            _context = context;
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
        public async Task<ActionResult<Personagem>> PostPersonagem(Personagem personagem)
        {
            _context.PersonagemSet.Add(personagem);
            await _context.SaveChangesAsync();

            return CreatedAtAction("GetPersonagem", new { id = personagem.Id }, personagem);
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

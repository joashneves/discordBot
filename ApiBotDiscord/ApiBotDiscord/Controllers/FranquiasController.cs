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
    public class FranquiasController : ControllerBase
    {
        private readonly FranquiaContext _context;

        public FranquiasController(FranquiaContext context)
        {
            _context = context;
        }

        // GET: api/Franquias
        [HttpGet]
        public async Task<ActionResult<IEnumerable<Franquia>>> GetFranquiaSet()
        {
            return await _context.FranquiaSet.ToListAsync();
        }

        // GET: api/Franquias/5
        [HttpGet("{id}")]
        public async Task<ActionResult<Franquia>> GetFranquia(int id)
        {
            var franquia = await _context.FranquiaSet.FindAsync(id);

            if (franquia == null)
            {
                return NotFound();
            }

            return franquia;
        }

        // PUT: api/Franquias/5
        // To protect from overposting attacks, see https://go.microsoft.com/fwlink/?linkid=2123754
        [HttpPut("{id}")]
        public async Task<IActionResult> PutFranquia(int id, Franquia franquia)
        {
            if (id != franquia.Id)
            {
                return BadRequest();
            }

            _context.Entry(franquia).State = EntityState.Modified;

            try
            {
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!FranquiaExists(id))
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

        // POST: api/Franquias
        // To protect from overposting attacks, see https://go.microsoft.com/fwlink/?linkid=2123754
        [HttpPost]
        public async Task<ActionResult<Franquia>> PostFranquia(Franquia franquia)
        {
            _context.FranquiaSet.Add(franquia);
            await _context.SaveChangesAsync();

            return CreatedAtAction("GetFranquia", new { id = franquia.Id }, franquia);
        }

        // DELETE: api/Franquias/5
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteFranquia(int id)
        {
            var franquia = await _context.FranquiaSet.FindAsync(id);
            if (franquia == null)
            {
                return NotFound();
            }

            _context.FranquiaSet.Remove(franquia);
            await _context.SaveChangesAsync();

            return NoContent();
        }

        private bool FranquiaExists(int id)
        {
            return _context.FranquiaSet.Any(e => e.Id == id);
        }
    }
}

using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using ApiBotDiscord.Domain.Models;
using ApiBotDiscord.Infraestrutura;
using Microsoft.AspNetCore.Authorization;

namespace ApiBotDiscord.Controllers
{
    [Authorize]
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
        [AllowAnonymous]
        [HttpGet]
        public async Task<ActionResult<IEnumerable<Franquia>>> GetFranquiaSet()
        {
            return await _context.FranquiaSet.ToListAsync();
        }
        [AllowAnonymous]
        [HttpGet("Pag")] // Retorna todas as franquias com paginação
        public async Task<ActionResult<IEnumerable<Franquia>>> GetPagFranquiaSet(int pageNumber = 0, int pageQuantity = 10)
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
                var totalRecords = await _context.FranquiaSet.CountAsync();

                // Obter registros paginados
                var franquiasPaginadas = await _context.FranquiaSet
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
                Console.WriteLine($"Erro ao obter as franquias paginadas: {ex.Message}");

                // Retornar status 500 com a mensagem de erro
                return StatusCode(500, new { mensagem = "Ocorreu um erro ao obter as franquias paginadas.", erro = ex.Message });
            }
        }


        // GET: api/Franquias/5
        [HttpGet("{id}")]
        [AllowAnonymous]
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

using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using ApiBotDiscord.Domain.Models;
using ApiBotDiscord.Infraestrutura;
using ApiBotDiscord.Domain.Dto;
using System.Text;
using System.Security.Cryptography;

namespace ApiBotDiscord.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class ContasController : ControllerBase
    {
        private readonly ContaContext _context;

        public ContasController(ContaContext context)
        {
            _context = context;
        }

        // GET: api/Contas
        [HttpGet]
        public async Task<ActionResult<IEnumerable<Conta>>> GetContaSet()
        {
            return await _context.ContaSet.ToListAsync();
        }

        // GET: api/Contas/5
        [HttpGet("{id}")]
        public async Task<ActionResult<Conta>> GetConta(int id)
        {
            var conta = await _context.ContaSet.FindAsync(id);

            if (conta == null)
            {
                return NotFound();
            }

            return conta;
        }

        // PUT: api/Contas/5
        // To protect from overposting attacks, see https://go.microsoft.com/fwlink/?linkid=2123754
        [HttpPut("{id}")]
        public async Task<IActionResult> PutConta(int id, Conta conta)
        {
            if (id != conta.Id)
            {
                return BadRequest();
            }

            _context.Entry(conta).State = EntityState.Modified;

            try
            {
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!ContaExists(id))
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

        // POST: api/Contas
        [HttpPost]
        public async Task<ActionResult<Conta>> PostConta(ContaDTO contaDto)
        {
            try
            {
                // Validação da senha com no mínimo 6 caracteres
                if (contaDto.Password.Length < 6)
                {
                    return BadRequest("A senha deve conter no mínimo 6 caracteres.");
                }

                // Converte o nome de usuário para minúsculas
                var userLower = contaDto.UserName.ToLower();

                // Validação para garantir que o user não tenha espaços
                if (userLower.Contains(" "))
                {
                    return BadRequest("O nome de usuário não pode conter espaços.");
                }

                // Verifica se já existe um usuário com o mesmo nome (em minúsculas)
                var userExists = await _context.ContaSet
                    .AnyAsync(c => c.UserName.ToLower() == userLower);
                if (userExists)
                {
                    return Conflict("Já existe uma conta com esse nome de usuário.");
                }

                // Verifica se já existe um usuário com o mesmo email
                var emailExists = await _context.ContaSet
                    .AnyAsync(c => c.Email == contaDto.Email);
                if (emailExists)
                {
                    return Conflict("Já existe uma conta com esse email.");
                }

                // Criação de uma nova conta com senha hash e nível 3
                var novaConta = new Conta
                {
                    UserName = userLower, // Armazena o nome de usuário em letras minúsculas
                    Name = contaDto.Name,
                    Email = contaDto.Email,
                    Password = HashPassword(contaDto.Password),
                    Nivel = 0 // Definindo o nível da conta como 3
                };

                _context.ContaSet.Add(novaConta);
                await _context.SaveChangesAsync();



                return CreatedAtAction("GetConta", new { id = novaConta.Id }, novaConta);
            }
            catch (Exception ex)
            {
                return StatusCode(StatusCodes.Status500InternalServerError, $"Erro inesperado: {ex.Message}");
            }
        }

        // DELETE: api/Contas/5
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteConta(int id)
        {
            var conta = await _context.ContaSet.FindAsync(id);
            if (conta == null)
            {
                return NotFound();
            }

            _context.ContaSet.Remove(conta);
            await _context.SaveChangesAsync();

            return NoContent();
        }
        [HttpPost("login")]
        public async Task<IActionResult> Login([FromBody] LoginDTO loginDto)
        {
            try
            {
                // Busca a conta no banco de dados com base no nome ou email
                var conta = await _context.ContaSet
                    .FirstOrDefaultAsync(c => c.UserName == loginDto.UserName);

                if (conta == null)
                {
                    return Unauthorized("Usuário incorreto.");
                }

                // Verificar se a senha fornecida é válida (comparando o hash)
                if (conta.Password != HashPassword(loginDto.Password))
                {
                    return Unauthorized("Senha incorreta.");
                }


                // Verificar se o nível da conta é 1 ou menor
                if (conta.Nivel > 1)
                {
                    return Ok("Conta autorizada.Mas não gerar token, O nível precisa ser 1 ou menor.");
                }

                // Gerar o token JWT
                return Ok();
            }
            catch (Exception ex)
            {
                return StatusCode(StatusCodes.Status500InternalServerError, $"Erro ao realizar login: {ex.Message}");
            }
        }
        // Função para realizar o hash da senha (exemplo com SHA256, substitua por bcrypt ou PBKDF2 em produção)
        private string HashPassword(string password)
        {
            using (var sha256 = SHA256.Create())
            {
                var bytes = sha256.ComputeHash(Encoding.UTF8.GetBytes(password));
                return Convert.ToBase64String(bytes);
            }
        }
        private bool ContaExists(int id)
        {
            return _context.ContaSet.Any(e => e.Id == id);
        }
    }
}

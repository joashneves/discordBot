using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using ApiBotDiscord.Domain.Models;
using ApiBotDiscord.Infraestrutura;
using System.Text;
using System.Security.Cryptography;
using Microsoft.AspNetCore.Authorization;
using ApiBotDiscord.Services;
using ApiBotDiscord.Domain.Dto.Conta;
using ApiBotDiscord.Domain.Dto;

namespace ApiBotDiscord.Controllers
{
    [Authorize]
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

        [HttpGet("Pag")] // Retorna todas as obras com paginação
        public async Task<ActionResult<IEnumerable<Conta>>> GetPagContaSet(int pageNumber, int pageQuantity)
        {
            return await _context.ContaSet.Skip(pageNumber * pageQuantity).Take(pageQuantity).ToListAsync();
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
        // GET: api/Contas/username
        [HttpGet("user/{userName}")]
        public async Task<ActionResult<Conta>> GetUser(string userName)
        {
            // Usa FirstOrDefaultAsync para buscar a conta com base no userName
            var conta = await _context.ContaSet
                .FirstOrDefaultAsync(c => c.UserName == userName); 

            if (conta == null)
            {
                return NotFound();
            }

            return conta;
        }

        [HttpPut("atualizar")]
        public async Task<IActionResult> AtualizarConta([FromBody] AtualizarSenhaDTO contaDto)
        {
            try
            {
                // Busca a conta no banco de dados com base no nome e email fornecidos
                var contaExistente = await _context.ContaSet
                    .FirstOrDefaultAsync(c => c.UserName == contaDto.UserName && c.Email == contaDto.Email);

                if (contaExistente == null)
                {
                    return NotFound("Conta não encontrada com os dados fornecidos.");
                }

                // Verificar se a senha antiga fornecida é válida (comparando o hash)
                if (contaExistente.Password != HashPassword(contaDto.SenhaAntiga))
                {
                    return BadRequest("Senha antiga incorreta.");
                }

                // Atualizar a senha e o nível da conta
                contaExistente.Password = HashPassword(contaDto.NovaSenha);

                // Salvar as alterações
                await _context.SaveChangesAsync();

                return Ok("Conta atualizada com sucesso.");
            }
            catch (DbUpdateConcurrencyException)
            {
                return StatusCode(StatusCodes.Status500InternalServerError, "Erro ao atualizar a conta.");
            }
            catch (Exception ex)
            {
                return StatusCode(StatusCodes.Status500InternalServerError, $"Erro inesperado: {ex.Message}");
            }
        }
        [HttpPut("resetar")]
        public async Task<IActionResult> ResetarSenha([FromBody] ContaUpdateDTO contaDto)
        {
            try
            {
                // Verificar se o usuário ADM tem permissões suficientes para redefinir a senha
                var contaAdm = await _context.ContaSet
                    .FirstOrDefaultAsync(c => c.UserName == contaDto.UserNameADM);

                if (contaAdm == null)
                {
                    return BadRequest("Usuário administrador não encontrado.");
                }
                if (contaAdm.Nivel >= 0)
                {
                    return BadRequest("O usuário administrador não tem permissão para redefinir senhas.");
                }

                // Busca a conta no banco de dados com base no nome e email fornecidos
                var contaExistente = await _context.ContaSet
                    .FirstOrDefaultAsync(c => c.UserName == contaDto.Username && c.Email == contaDto.Email);

                if (contaExistente == null)
                {
                    return NotFound("Conta não encontrada com os dados fornecidos.");
                }

                // Atualizar a senha e o nível da conta
                contaExistente.Password = HashPassword(contaDto.NovaSenha);
                contaExistente.Nivel = contaDto.NovoNivel;

                // Salvar as alterações
                await _context.SaveChangesAsync();

                return Ok("Senha e nível da conta atualizados com sucesso.");
            }
            catch (DbUpdateConcurrencyException)
            {
                return StatusCode(StatusCodes.Status500InternalServerError, "Erro ao atualizar a conta.");
            }
            catch (Exception ex)
            {
                return StatusCode(StatusCodes.Status500InternalServerError, $"Erro inesperado: {ex.Message}");
            }
        }

        // POST: api/Contas
        [HttpPost]
        public async Task<ActionResult<Conta>> PostConta(ContaDTO contaDto)
        {
            try
            {
                // Verificar se o usuário ADM tem permissões suficientes para redefinir a senha
                var contaAdm = await _context.ContaSet
                    .FirstOrDefaultAsync(c => c.UserName == contaDto.UserNameADM);
                // Validação da senha com no mínimo 6 caracteres
                if (contaDto.Password.Length < 6)
                {
                    return BadRequest("A senha deve conter no mínimo 6 caracteres.");
                }
                if (contaAdm == null)
                {
                    return BadRequest("Usuário administrador não encontrado.");
                }
                if (contaAdm.Nivel >= 1)
                {
                    return BadRequest("O usuário administrador não tem permissão para redefinir senhas.");
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
                    Nivel = 1 // Definindo o nível da conta como 3
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
        [AllowAnonymous]
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
                if (conta.Nivel > 2)
                {
                    return Ok("Conta autorizada.Mas não gerar token, O nível precisa ser 1 ou menor.");
                }

                // Gerar o token JWT
                var token = TokenGeneration.GenerateToken(conta);
                return Ok(new { Token = token });
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

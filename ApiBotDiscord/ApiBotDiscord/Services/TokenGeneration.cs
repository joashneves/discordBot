using ApiBotDiscord.Domain.Models;
using Microsoft.EntityFrameworkCore.Metadata.Internal;
using System.Security.Claims;
using System.Text;
using System.IdentityModel.Tokens.Jwt;
using Microsoft.IdentityModel.Tokens;
namespace ApiBotDiscord.Services
{
    public class TokenGeneration
    {

            public static object GenerateToken(Conta conta)
            {
                var secretKey = Environment.GetEnvironmentVariable("SECRET_KEY"); // Obtém a chave do .env
                var key = Encoding.ASCII.GetBytes(secretKey);
                var tokenDescriptor = new SecurityTokenDescriptor
                {
                    Subject = new ClaimsIdentity(new[]
                    {
            new Claim(ClaimTypes.Name, conta.Name),
            new Claim(ClaimTypes.Email, conta.Email),
                    new Claim("Nivel", conta.Nivel.ToString()) // Adicionando o nível da conta ao token
        }),
                    Expires = DateTime.UtcNow.AddHours(2), // O token vai expirar em 2 horas
                    SigningCredentials = new SigningCredentials(new SymmetricSecurityKey(key), SecurityAlgorithms.HmacSha256Signature)
                };

                var tokenHandler = new JwtSecurityTokenHandler();
                var token = tokenHandler.CreateToken(tokenDescriptor);
                var tokenString = tokenHandler.WriteToken(token);

                return new { token = tokenString };

            }
        
    }
}

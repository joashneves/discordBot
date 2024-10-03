using ApiBotDiscord.Domain.Models;
using Microsoft.EntityFrameworkCore;

namespace ApiBotDiscord.Infraestrutura
{
    public class PersonagemContext : DbContext
    {
        private IConfiguration _configuration;
        public DbSet<Personagem> PersonagemSet { get; set; }

        public PersonagemContext(IConfiguration configuration, DbContextOptions<PersonagemContext> options)
            : base(options)
        {
            _configuration = configuration ?? throw new ArgumentNullException(nameof(configuration));
        }

        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            var connectionString = _configuration.GetConnectionString("MySQLData");
            optionsBuilder.UseMySQL(connectionString);
        }
    }
}

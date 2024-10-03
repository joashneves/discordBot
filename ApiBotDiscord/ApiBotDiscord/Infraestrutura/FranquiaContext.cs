using ApiBotDiscord.Domain.Models;
using Microsoft.EntityFrameworkCore;
using System.Collections.Generic;

namespace ApiBotDiscord.Infraestrutura
{
    public class FranquiaContext : DbContext
    {
        private IConfiguration _configuration;
        public DbSet<Franquia> FranquiaSet { get; set; }

        public FranquiaContext(IConfiguration configuration, DbContextOptions<FranquiaContext> options)
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

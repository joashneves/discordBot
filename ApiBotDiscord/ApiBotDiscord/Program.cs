using ApiBotDiscord.Infraestrutura;
using dotenv.net;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.IdentityModel.Tokens;
using Microsoft.OpenApi.Models;
using System.Text;

var builder = WebApplication.CreateBuilder(args);

// Carregar vari�veis do arquivo .env
DotEnv.Load(); // Adicionando esta linha para carregar as vari�veis de ambiente


// Add services to the container.
// JWT
var secretKey = Environment.GetEnvironmentVariable("SECRET_KEY"); // Obt�m a chave do .env
if (string.IsNullOrEmpty(secretKey))
{
    secretKey = "your-default-secret-key";  // Chave padrão
}
var key = Encoding.ASCII.GetBytes(secretKey);
builder.Services.AddAuthentication(x =>
{
    x.DefaultAuthenticateScheme = JwtBearerDefaults.AuthenticationScheme;
    x.DefaultChallengeScheme = JwtBearerDefaults.AuthenticationScheme;
}).AddJwtBearer(x =>
{
    x.RequireHttpsMetadata = false;
    x.SaveToken = true;
    x.TokenValidationParameters = new TokenValidationParameters
    {
        ValidateIssuerSigningKey = true,
        IssuerSigningKey = new SymmetricSecurityKey(key),
        ValidateIssuer = false,
        ValidateAudience = false
    };
});

builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new OpenApiInfo { Title = "BoletimInterno API", Version = "v1" });

    // Adicionando o esquema de seguran�a JWT
    c.AddSecurityDefinition("Bearer", new OpenApiSecurityScheme
    {
        Description = "Autoriza��o JWT usando o esquema Bearer. \n\n" +
                      "Insira 'Bearer' [espa�o] e depois o token JWT.\n\n" +
                      "Exemplo: 'Bearer 12345abcdef'",
        Name = "Authorization",
        In = ParameterLocation.Header,
        Type = SecuritySchemeType.ApiKey,
        Scheme = "Bearer"
    });

    c.AddSecurityRequirement(new OpenApiSecurityRequirement()
            {
                {
                    new OpenApiSecurityScheme
                    {
                        Reference = new OpenApiReference
                        {
                            Type = ReferenceType.SecurityScheme,
                            Id = "Bearer"
                        },
                        Scheme = "oauth2",
                        Name = "Bearer",
                        In = ParameterLocation.Header,
                    },
                    new List<string>()
                }
            });
});
// Configure CORS
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowSpecificOrigin",
        builder =>
        {
            builder.WithOrigins("http://localhost:5173") // Substitua com o IP ou dom�nio espec�fico
                   .AllowAnyHeader()
                   .AllowAnyMethod(); // Permite qualquer m�todo para esse site espec�fico
        });

    options.AddPolicy("AllowGetOnly",
        builder =>
        {
            builder.AllowAnyOrigin() // Permite qualquer dom�nio
                   .AllowAnyHeader()
                   .WithMethods("GET"); // Permite apenas requisi��es GET
        });
});

builder.Services.AddControllers();
// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

builder.Services.AddDbContext<FranquiaContext>();
builder.Services.AddDbContext<PersonagemContext>();
builder.Services.AddDbContext<ContaContext>();

var app = builder.Build();


// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();

}

app.UseHttpsRedirection();

app.UseCors(policy =>
{
    policy.WithOrigins("http://localhost:5173") // Para este site espec�fico
          .AllowAnyHeader()
          .AllowAnyMethod() // Permitir qualquer m�todo
          .SetIsOriginAllowedToAllowWildcardSubdomains()
          .AllowCredentials(); // Permitir envio de cookies (se necess�rio)
});


app.UseAuthorization();

app.MapControllers();

app.Run();

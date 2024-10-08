using ApiBotDiscord.Infraestrutura;
using dotenv.net;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.IdentityModel.Tokens;
using Microsoft.OpenApi.Models;
using System.Text;

var builder = WebApplication.CreateBuilder(args);

// Carregar variáveis do arquivo .env
DotEnv.Load(); // Adicionando esta linha para carregar as variáveis de ambiente


// Add services to the container.
// JWT
var secretKey = Environment.GetEnvironmentVariable("SECRET_KEY"); // Obtém a chave do .env
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

    // Adicionando o esquema de segurança JWT
    c.AddSecurityDefinition("Bearer", new OpenApiSecurityScheme
    {
        Description = "Autorização JWT usando o esquema Bearer. \n\n" +
                      "Insira 'Bearer' [espaço] e depois o token JWT.\n\n" +
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
            builder.WithOrigins("https://meusite.com") // Substitua com o IP ou domínio específico
                   .AllowAnyHeader()
                   .AllowAnyMethod(); // Permite qualquer método para esse site específico
        });

    options.AddPolicy("AllowGetOnly",
        builder =>
        {
            builder.AllowAnyOrigin() // Permite qualquer domínio
                   .AllowAnyHeader()
                   .WithMethods("GET"); // Permite apenas requisições GET
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
    policy.WithOrigins("https://meusite.com") // Para este site específico
          .AllowAnyHeader()
          .AllowAnyMethod() // Permitir qualquer método
          .SetIsOriginAllowedToAllowWildcardSubdomains()
          .AllowCredentials(); // Permitir envio de cookies (se necessário)
});


app.UseAuthorization();

app.MapControllers();

app.Run();

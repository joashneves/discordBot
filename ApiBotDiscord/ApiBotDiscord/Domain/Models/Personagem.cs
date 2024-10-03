namespace ApiBotDiscord.Domain.Models
{
    public class Personagem
    {
        public int Id { get; set; }
        public int Id_Franquia { get; set; }
        public string Name { get; set; }
        public string Gender { get; set; }
        public string CaminhoArquivo { get; set; }
    }
}

namespace ApiBotDiscord.Domain.Models
{
    public enum GenderEnum
    {
        Feminino,
        Masculino,
        NaoBinario,
        Fluido,
        Outros
    }
    public class Personagem
    {
        public int Id { get; set; }
        public int Id_Franquia { get; set; }
        public string Name { get; set; }
        public GenderEnum Gender { get; set; }
        public string CaminhoArquivo { get; set; }
    }
}

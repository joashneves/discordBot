namespace ApiBotDiscord.Domain.Dto
{
    public class CadastrarFranquiaDTO
    {
        public string Name { get; set; }
        public string Description { get; set; }
        public string Creator { get; set; }
        public string Attachment { get; set; }
        public DateTime Data_Published { get; set; }
    }
}

namespace ApiBotDiscord.Domain.viewmodels
{
    public class PersonagemViewModel
    {
        public int Id { get; set; }
        public int Id_Franquia { get; set; }
        public string Name { get; set; }
        public string Gender { get; set; }
        public IFormFile ArquivoPersonagem { get; set; }
    }
}

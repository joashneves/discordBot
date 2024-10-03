namespace ApiBotDiscord.Domain.Models
{
    public class Franquia
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public string Description { get; set; }
        public string Creator { get; set; }
        public string Attachment {  get; set; }
        public DateTime Data_Published { get; set; }
    }
}

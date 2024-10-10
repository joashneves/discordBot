namespace ApiBotDiscord.Domain.Dto
{
    public class ContaUpdateDTO
    {
        public string UserNameADM { get; set; }     // Nome de usuário
        public string Username { get; set; }     // Nome de usuário
        public string Email { get; set; }    // Email da conta
        public string SenhaAntiga { get; set; } // Senha antiga da conta
        public string NovaSenha { get; set; }   // Nova senha a ser atualizada
        public int NivelNovo { get; set; }      // Novo nível da conta
    }

}

namespace ApiBotDiscord.Domain.Dto.Conta
{
    public class AtualizarSenhaDTO
    {
        public string UserName { get; set; }
        public string Email { get; set; }
        public string SenhaAntiga { get; set; } // Senha antiga da conta
        public string NovaSenha { get; set; }   // Nova senha a ser atualizada
    }
}

# Etapa de construção
FROM node:20 AS build

# Diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos do projeto para o contêiner
COPY . .

# Instala as dependências do projeto
RUN npm install

# Gera os arquivos estáticos de produção
RUN npm run build

# Etapa de execução
FROM nginx:1.25

# Remove o arquivo de configuração padrão do nginx
RUN rm /etc/nginx/conf.d/default.conf

# Copia o arquivo de configuração customizado para o nginx
COPY nginx.conf /etc/nginx/conf.d

# Copia os arquivos estáticos para o diretório de saída do nginx
COPY --from=build /app/dist /usr/share/nginx/html

# Porta exposta pelo contêiner
EXPOSE 80

# Comando de entrada para iniciar o nginx
CMD ["nginx", "-g", "daemon off;"]

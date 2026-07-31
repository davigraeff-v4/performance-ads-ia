---
title: "Sobre usuários do sistema no Meta Business Suite"
url: "https://www.facebook.com/business/help/327596604689624"
categoria: "11-portfolio-negocios"
fonte: "Central de Ajuda da Meta para Empresas"
idioma: "pt-BR"
extraido_em: "2026-07-31"
---

# Sobre usuários do sistema no Meta Business Suite

Os usuários do sistema representam servidores ou programas de software que fazem chamadas de API para ativos gerenciados por um portfólio empresarial no Meta Business Suite.

## Há dois tipos de usuários do sistema

- **Usuário administrador do sistema**: pode criar usuários do sistema, adicionar contas, atribuir permissões e muito mais.
- **Usuário do sistema comum**: só pode acessar os ativos para os quais tem permissão.

## Boas práticas

- Crie um usuário do sistema para cada tipo de acesso necessário. Dê a esses usuários acesso apenas aos ativos relevantes e use-os para a maioria das chamadas de API.
- Use o usuário administrador do sistema para manter as funções corretas de forma programática. Assim, se um token de usuário do sistema for comprometido, ele terá escopo limitado e não conseguirá comprometer mais permissões.
- Limite o uso do usuário administrador do sistema a ações administrativas, como atribuir permissões. Por ter a maior quantidade de permissões, o token do usuário administrador do sistema deve ser cuidadosamente protegido.

/**
     * Insere um torcedor na base de dados, verificando consistência dos dados
     * 
     * @param {string} nome - Nome do torcedor para cadastro 
     * @param {string} cpf - CPF do torcedor para cadastro
     * @param {string} email - Email do torcedor para cadastro
     * @param {string} nivel_socio - Nível de Sócio (Vip, Vip+ ou Fanático)
     */
async function inserir_torcedor(nome, cpf, email, nivel_socio){

    const args = [nome, cpf, email, nivel_socio]

    const todosValidos = args.every(arg => typeof arg === 'string' && arg.trim() !== '')

    if (!todosValidos){
        console.warn("Aviso: Presenca de argumento invalido");
        return null;
    }
    
    const verifica_cpf = await db.Torcedor.findOne({cpf:cpf})
    
    if (verifica_cpf){
        console.warn("CPF ja cadastrado no banco de dados.")
        return null;
    }
    
    const verifica_email = await db.Torcedor.findOne({email:email})
    
    if (verifica_email){
        console.warn("Email ja cadastrado no banco de dados.")
        return null;
    }
    
    try {
        const res = await db.Torcedor.insertOne({ 
            nome: nome,
            cpf: cpf,
            email: email,
            nivel_socio: nivel_socio
        });
        
        console.log(`Usuario ${nome} inserido com sucesso!`);
    }
    catch(err){
        console.error(`Algo de errado aconteceu: ${err}`);
    }
}

/**
     * Lista os torcedores cadastrados na base de dados
     * 
     * Não recebe parâmetros
     */
async function mostrar_torcedores(){
    try{
        res = await db.Torcedor.find();
        console.log(res)
        console.log("Torcedores listados com sucesso!");
    }
    catch(err){
        console.error(`Algo de errado aconteceu: ${err}`);
    }
}

/**
     * Atualiza os dados de um torcedor, buscando pelo CPF
     * 
     * @param {string} cpf - CPF do torcedor para identificacao na DB
     * @param {string} novo_nome - Novo nome para ser alterado na base de dados
     * @param {string} novo_cpf - Novo CPF para ser alterado na base de dados
     * @param {string} novo_email - Novo email para ser alterado na base de dados
     * @param {string} novo_nivel - Novo nivel de socio para ser alterado na base de dados
     */
async function atualizar_torcedor(cpf, novo_nome, novo_cpf, novo_email, novo_nivel){    

    const args = [cpf, novo_nome, novo_cpf, novo_email, novo_nivel]

    const todosValidos = args.every(arg => typeof arg === 'string' && arg.trim() !== '')

    if (!todosValidos){
        console.warn("Aviso: Presenca de argumento invalido");
        return null;
    }
    
    const verifica = await db.Torcedor.findOne({cpf: cpf})
    
    if (!verifica){
        console.warn("Aviso: O torcedor nao foi encontrado.");
        return null;
    }
    try{
        const res = db.Torcedor.updateOne({cpf: cpf}, {$set: {
            nome: novo_nome, 
            cpf: novo_cpf, 
            email: novo_email, 
            nivel_socio: novo_nivel
        }})
        
        console.log(`Torcedor ${verifica.nome} atualizado!`)
    }
    catch(err){
        console.error(`Algo de errado aconteceu: ${err}`)
    }
}

/**
     * Deleta um torcedor da base de dados, buscando pelo CPF
     * 
     * @param {string} cpf - CPF do torcedor para identificacao na DB
     */
async function deletar_torcedor(cpf){
    if (!cpf){
        console.warn("Aviso: CPF nao fornecido.");
        return null;
    }

    const verifica = await db.Torcedor.findOne({cpf: cpf})

    if (!verifica){
        console.warn("Aviso: O Torcedor nao encontrado.")
        return null;
    }
    try{
        const res = db.Torcedor.deleteOne({cpf: cpf})
        console.log(`Torcedor ${verifica.nome} removido!`)
    }
    catch(err){
        console.error(`Algo de errado aconteceu: ${err}`)
    }
}
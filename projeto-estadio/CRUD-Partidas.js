/**
     * Insere um torcedor na base de dados, verificando consistência dos dados
     * 
     * @param {{mandante: string, visitante: string}} times - Nomes dos times - {mandante: Time A, visitante: Time B}
     * @param {Date} data - Data no formato Date
     * @param {number} preco_base - Preço base do ingresso, sem nenhum tipo de desconto
     */
async function inserir_partida(times, data, preco_base){
    if ((!times) || (!data) || (!preco_base)){
        console.warn("Aviso: Presenca de argumento invalido.");
        return null;
    }
   
    const verifica_data = await db.Partida.findOne({data:data})
    
    if (verifica_data){
        console.warn("Data reservada para outro evento.")
        return null;
    }

    try {
        const res = await db.Partida.insertOne({ 
            times: times,
            data: data,
            estadio: "Castelao",
            preco_base: preco_base
            });
            
        console.log(`Partida ${times} inserida com sucesso!`);
    }
    catch(err){
        console.error(`Algo de errado aconteceu: ${err}`);
    }
}

/**
     * Lista as partidas cadastrados na base de dados
     * 
     * Não recebe parâmetros
     */
async function mostrar_partidas(){
    try{
        const res = await db.Partida.find()
        console.log(res)
        console.log("Partidas listadas com sucesso.")
    }
    catch(err){
        console.error(`Algo de errado aconteceu: ${err}`)
    }
}

/**
     * Atualiza os dados de uma partida na base de dados
     * 
     * @param {Date} data - Data no formato Date para consulta
     * @param {{mandante: string, visitante: string}} novo_times - Nomes dos novos times - {mandante: Time A, visitante: Time B}
     * @param {Date} nova_data - Nova data para o jogo
     * @param {number} novo_preco - Novo Preço base do ingresso, sem nenhum tipo de desconto
     * @todo Existe um problema de lógica aqui, na nova data pode já ter uma partida marcada
     */
async function atualizar_partida(data, novo_times, nova_data, novo_preco){
    if ((!data) || (!novo_times) || (!nova_data) || (!novo_preco)){
        console.warn("Aviso: Presenca de argumento invalido.");
        return null;
    }

    const verifica = await db.Partida.findOne({data: data})

    if (!verifica){
        console.warn("Aviso: A partida nao foi encontrada.");
        return null;
    }
    try{
        const res = db.Partida.updateOne({data: data}, {$set: {
            times: novo_times, 
            data: nova_data, 
            estadio: "Castelao", 
            preco_base: novo_preco
        }})
        
        console.log(`Partida ${verifica.times} atualizada!`)
    }
    catch(err){
        console.error(`Algo de errado aconteceu: ${err}`)
    }
}

/**
     * Deleta um torcedor da base de dados, buscando pelo CPF
     * 
     * @param {Date} data - Data do jogo para identificacao na DB
     */
async function deletar_partida(data){
    if (!data){
        console.warn("Data nao fornecida.");
        return null;
    }
    
    const verifica = await db.Partida.findOne({data: data})
    
    if (!verifica){
        console.warn("Aviso: Partida nao encontrada.")
        return null;
    }
    try{
        const res = db.Partida.deleteOne({data: data})
        console.log(`Partida ${verifica.times} removida com sucesso!`)
    }
    catch(err){
        console.error(`Algo de errado aconteceu: ${err}`)
    }
}
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
            
        console.log("Partida ${times} inserida com sucesso!");
    }
    catch(err){
        console.error("Algo de errado aconteceu: ${err}");
    }
}

async function mostrar_partidas(){
    try{
        const res = await db.Partida.find()
        console.log(res)
        console.log("Partidas listadas com sucesso.")
    }
    catch(err){
        console.error("Algo de errado aconteceu: ${err}")
    }
}

async function atualizar_partida(data, novo_times, novo_data, novo_preco){
    if ((!data) || (!novo_times) || (!novo_data) || (!novo_preco)){
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
            data: novo_data, 
            estadio: "Castelao", 
            preco_base: novo_preco
        }})
        
        console.log("Partida ${verifica.times} atualizada!")
    }
    catch(err){
        console.error(`Algo de errado aconteceu: ${err}`)
    }
}

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
        console.log("Partida ${verifica.times} removida com sucesso!")
    }
    catch(err){
        console.error("Algo de errado aconteceu: ${err}")
    }
}
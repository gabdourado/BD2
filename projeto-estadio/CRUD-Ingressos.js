async function create_ingresso(cpf_usuario, data_partida){
    if ((!cpf_usuario) || (!data_partida)){
        console.warn("Aviso: Presenca de argumento invalido.");
        return null;
    }
    
    const partida = await db.Partida.findOne({data: data_partida})
    const socio = await db.Torcedor.findOne({cpf: cpf_usuario})

    if (!socio){
        console.warn("Torcedor nao encontrado.")
        return null;
    }

    if (!partida){
        console.warn("Partida nao encontrada.")
        return null;
    }
   
    const ingresso_usuario_id = await db.Ingressos.findOne({id_usuario: socio._id})
    const ingresso_partida_id = await db.Ingressos.findOne({id_partida: partida._id})
    
    if (ingresso_usuario_id && ingresso_partida_id){
        console.warn("Voce ja comprou entrada para este jogo.")
        return null;
    }
    
    let desconto = 0;
    let preco_pago = partida.preco_base;


    if (socio.nivel_socio == "Fanatico"){
        desconto = partida.preco_base * 0.30
    }
    else if (socio.nivel_socio == "Vip+"){
        desconto = partida.preco_base * 0.20
    }
    else if (socio.nivel_socio == "Vip"){
        desconto = partida.preco_base * 0.10
    }
    
    preco_pago -= desconto
    
    try{
        const res = db.Ingressos.insertOne({ 
            id_usuario: socio._id,
            id_partida: partida._id,
            preco_pago: preco_pago,
            valor_desconto: desconto,
            data_compra: new Date()
            })
            
        console.log("Ingresso ${res.insertedId} comprado!")
    }
    catch(err){
        console.error("Algo de errado aconteceu: ${err}")
        return null;
    }
}

async function mostrar_ingressos(){
    try{
        const res = await db.Ingressos.find()
        console.log(res)
        console.log("Ingressos listados com sucesso.")
    }
    catch(err){
        console.error("Algo de errado aconteceu: ${err}")
        return null;
    }
}

async function deletar_ingresso(cpf, data){
    if ((!cpf) || (!data)){
        console.warn("Aviso: Presenca de argumento invalido.");
        return null;
    }
    
    const torcedor = await db.Torcedor.findOne({cpf: cpf})
    
    if (!torcedor){
        console.warn("Torcedor nao encontrado.")
        return null;
    }

    const partida = await db.Partida.findOne({data: data})

    if (!partida){
        console.warn("Partida nao encontrada.")
        return null;
    }

    const ingresso = await db.Ingressos.findOne({
    id_partida: partida._id, 
    id_usuario: torcedor._id
    })
    
    if(!ingresso){
        console.warn("Ingresso nao encontrado.")
        return null;
    }
    try{
        const res = await db.Ingressos.deleteOne({_id:ingresso._id})
        console.log("Ingresso ${ingresso._id} deletado.")
    }
    catch(err){
        console.error("Algo de errado aconteceu: ${err}")
        return null;
    }
}
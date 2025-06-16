/**
 * Operação que estima o lucro total em um determiando mês
 * Não rececebe parâmetros
 * @example faturamento_por_jogo()

 */
async function faturamento_por_jogo() {  
    try{
        const res = db.Ingressos.aggregate([
        {
            $lookup: {
                from: "Partida",
                localField: "id_partida",
                foreignField: "_id",
                as: "partida_info"
            }
        },
        {
            $unwind: "$partida_info"
        },
        {
            $group: {
            _id: "$partida_info.times",
            total_renda: { $sum: "$preco_pago" },
            total_ingressos: { $sum: 1 }
            }
        }   
    ])
        console.log(res)
    }
    catch(err){
        console.error(`Algo de errado aconteceu: ${err}`)
        return null;
    }
}

/**
 * Operação que estima o lucro total em um determiando mês
 * @param {Date} inicio - Data inicial da analise
 * @param {Date} fim - Data final da analise
 * @example total_ingressos("2025-06-01T00:00:00.000Z", "2025-06-30T00:00:00.000Z")

 */
async function total_ingressos(inicio, fim) {

    if (!inicio || !fim) {
        console.warn("Aviso: Presenca de argumento invalido.");
        return null;
    }
    
    try{
        const res = await db.Ingressos.aggregate([
        {
            $match: {
                data_compra: {
                $gte: ISODate(inicio),
                $lt: ISODate(fim)
                }
            }
        },
        {
            $group: {
            _id: 0,
            total_renda: { $sum: "$preco_pago"},
            total_ingressos: { $sum: 1 }
            }
        }
    ])
        console.log(res)
    }
    catch(err){
        console.error(`Algo de errado aconteceu: ${err}`)
        return null;
    }
}

/**
 * Operação que retorna quantos ingressos cada torcedor comprou no total (em ordem alfabética)
 * Não recebe parâmetros
 * @todo Ainda não fiz!
 * @example count_ingressos()
 */

async function count_ingressos() {
    
    try{
        const res = await db.Ingressos.aggregate([

        ])

        console.log(res)
    }
    catch(err){
        console.error(`Algo de errado aconteceu: ${err}`)
        return null;
    }
}


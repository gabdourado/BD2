# Anotações sobre MongoDB

## Comandos no MongoDB

### "Criar" um Banco de Dados
Não existe comando para criar um banco de dados em Mongodb, para isso usamos o comando `use`?

```mongodb
use Castelao
```

### "Criar" Collections
Existe uma maneira de criar uma collection de forma explícita, porém na maioria dos casos criamos uma durante a inserção de documentos:

```mongodb
db.torcedores.insertOne({
    nome: 'Gabriel',
    cpf: '111.444.555-99',
    email: 'gab.dourado@gamil.com',
    nivel_socio: 'Vip+'
})
```


```mongodb
db.partidas.insertOne({
    times: {

    }
})
```


```mongodb
db.torcedor.insertOne({
    nome: 'Gabriel',
    cpf: '111.444.555-99',
    email: 'gab.dourado@gamil.com',
    nivel_socio: 'Vip+'
})
```


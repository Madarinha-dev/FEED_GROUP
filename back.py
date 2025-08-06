from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc, desc
from flask_migrate import Migrate
import base64
import os
import click


# PONTO DE PARTIDA PARA RECUPERAÇÃO
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

SUPABASE_DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'instance', 'banco.db'))
# SUPABASE_DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql+psycopg2://postgres:fhellype1984@db.yvsflzozsbvxlkulmlrg.supabase.co:5432/postgres')


app.config['SQLALCHEMY_DATABASE_URI'] = SUPABASE_DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

lista = []


# postgresql://postgres:fhellype1984@db.yvsflzozsbvxlkulmlrg.supabase.co:5432/postgres









class Funcionario(db.Model):
    __tablename__ = 'funcionarios_cadastrados'
    id_funcionario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255))
    senha = db.Column(db.String(255))
    cpf = db.Column(db.String(255))
    funcao = db.Column(db.String(255))


class Registro(db.Model):
    __tablename__ = 'registro'
    id_registro = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_atividade = db.Column(db.Integer)
    legenda = db.Column(db.String(255))
    img = db.Column(db.LargeBinary)


class Atividade(db.Model):
    __tablename__ = 'atividades'
    id_atividade = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo_de_servico = db.Column(db.String(255))
    descricao = db.Column(db.String(255))
    quem = db.Column(db.String(255))
    armazenna = db.Column(db.String(255))
    empresa = db.Column(db.String(255))
    data = db.Column(db.String(255))
    status = db.Column(db.String(255), default='0')


class Frequencia(db.Model):
    __tablename__ = 'frequencia'
    id_frequencia = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_funcionario = db.Column(db.Integer, db.ForeignKey('funcionarios_cadastrados.id_funcionario'), nullable=True)
    nome = db.Column(db.String(255))
    data = db.Column(db.String(255))
    hora = db.Column(db.String(255))
    funcao = db.Column(db.String(255))




@app.route('/')
def index():
    print(')')
    print(')')
    print(')')
    print('FUNÇÃO >>> / <<<')
    print(')')
    print(')')
    print(')')
    return render_template('index.html')


@app.route('/test_db')
def test_db():
    try:
        # Tenta contar o número de funcionários para verificar a conexão com o DB
        num_funcionarios = db.session.query(Funcionario).count()
        return f"Servidor rodando e conectado ao Supabase com sucesso! Número de funcionários: {num_funcionarios}"
    except Exception as e:
        return f"Servidor rodando, mas houve um erro ao conectar ao banco de dados: {e}"



@app.route('/excluirRegistro', methods=['POST'])
def excluirRegistro():
    try:
        dados = request.get_json()
        print(f'Dados: {dados}')
        alt = int(dados['alt'])

        registro_a_excluir = Registro.query.get(alt)

        if registro_a_excluir:
            db.session.delete(registro_a_excluir)
            db.session.commit()
            print('REGISTRO DELETADO')
            return jsonify({
                'success':True,
                'msg': 'REGISTRO DELETADO COM SUCCESS'
            }), 200
        else:
            print(f'ERRO: Registro com ID {alt} não encontrado')
            return jsonify({
                'success':False,
                'msg':'Erro: Registro não encontrado'
            }), 404
    except Exception as erro:
        db.session.rollback()
        print('ERRO DETECTADO FUNÇÃO: FUNÇÃO EXCLUIR REGISTRO')
        print(f'O tipo de Erro: {type(erro)}')
        print(f'Descrição do erro: {str(erro)}')

        return jsonify({
            'success':False,
            'msg':'Erro ao tentar excluir o registro'
        }), 500
    




    

@app.route('/registro_das_atividades_adm', methods=['GET'])
def exibir_registro():
    try:
        print('oi')
        registros = Registro.query.order_by(Registro.id_atividade).all()
        lista_json = []

        for registro in registros:
            dicionario = {
                'id_registro':registro.id_registro,
                'id_atividade': registro.id_atividade,
                'legenda': registro.legenda,
                'foto': f"data:image/jpeg;base64,{base64.b64encode(registro.img).decode('utf-8')}"
            }
            lista_json.append(dicionario)

        print('Comunicação realizada com a API')
        return jsonify({
            'success':True,
            'msg':'Comunicação realizada com a API',
            'dados':lista_json
        }), 200


    except Exception as erro:
        db.session.rollback()
        print('ERRO DETECTADO, FUNÇÃO: REGISTRO DAS ATIVIDADES ADM')
        print(f'TIPO DO ERRO: {type(erro)}')
        print(f'DESCRIÇÃO: {str(erro)}')

        return jsonify({
            'success':False,
            'msg':'ERRO ao exibir os registros'
        }), 500







@app.route('/album_de_fotos_das_atividades', methods=['POST'])
def album():
    try: 
        dados = request.get_json()

        for a in dados:
            print('')
            print('=')
            print(f'ID: {a["id"]}')
            print(f'LEGENDA: {a["legenda"]}')
            print('=')
            
            id_atividade = int(a['id'])
            legenda = str(a['legenda'])

            imagem_base64_com_prefixo = a['imagemData']
            _, encoded_image = imagem_base64_com_prefixo.split(',', 1)
            imagem_bytes = base64.b64decode(encoded_image)

            novo_registro = Registro(
                id_atividade=id_atividade,
                legenda=legenda,
                img=imagem_bytes
            )

            db.session.add(novo_registro)
        db.session.commit()
        
        return jsonify({
            "success":True,
            "msg":"REGISTRO ENVIADO COM SUCCESS"
        }), 200
    
    except Exception as erro:
        db.session.rollback()
        print('ERRO DETECTADO, FUNÇÃO: ALBUM')
        print(f'TIPO DE ERRO: {type(erro)}')
        print(f'DESCRIÇÃO DO ERRO: {str(erro)}')

        return jsonify({
            "success":False,
            "msg":"ERRO AO ENVIAR SEUS REGISTROS"
        }), 500






@app.route('/exibir_tabela_frequencia', methods=['GET'])
def exibir_tabela_frequencia():
    try:
        frequencias = Frequencia.query.all()
        nova_lista = []

        for a in frequencias:
            dicionario = {
                'id':a.id_frequencia,
                'nome':a.nome,
                'data':a.data,
                'tempo':a.hora,
                'funcao':a.funcao
            }
            nova_lista.append(dicionario)

        print('FREQUÊNCIA COLETADA')
        return jsonify({
            'success':True,
            'msg':'Frequência coletada',
            'dados':nova_lista
        }), 200
    
    except Exception as erro:
        db.session.rollback()

        print(f'ERRO DETECTADO, FUNÇÃO: EXIBIR A TABELA FREQUÊNCIA')
        print(f'TIPO DE ERRO: {type(erro)}')
        print(f'DESCRIÇÃO DO ERRO: {str(erro)}')
        print('=')

        return jsonify({
            'success':False,
            'msg':'Erro ao coletar a frequência da tabela'
        }), 500






@app.route('/limparFrequencia', methods=['POST'])
def limparFrequencia():
    try:
        db.session.query(Frequencia).delete()
        db.session.commit()

        return jsonify({
            'success':True,
            'msg':"Frequência Limpa com successo"
        }),200
    
    except Exception as erro:

        db.session.rollback()

        print('=============================================')
        print(f'ERRO DETECTADO, FUNÇÃO: LIMPAR FREQUÊNCIA')
        print(f'TIPO DO ERRO: {type(erro)}')
        print(f'DESCRIÇÃO: {str(erro)}')
        print('=============================================')

        return jsonify({
            "success": False,
            "msg": "Erro ao Limpar a frequência"
        }), 500


       


@app.route('/frequencia', methods=['POST'])
def frequencia():

    try:
        registro = request.get_json()
        nome = registro.get('nome')

        if nome == 'none':

            data_registro = f"{str(registro.get('dia'))}/{str(registro.get('mes'))}/{str(registro.get('ano'))}"
            tempo_registro = f"{str(registro.get('hora'))}:{str(registro.get('minuto'))}:{str(registro.get('segundo'))}"

            funcao = 'adm'

            nova_frequencia = Frequencia(
                id_funcionario=None,
                nome=nome,
                data=data_registro,
                hora=tempo_registro,
                funcao=funcao
            )

            db.session.add(nova_frequencia)
            db.session.commit()


            return jsonify({
                'success':True,
                'msg':'ACESSO LIBERADO PARA A TELA ADM - NONE',
                'funcao':'adm'
            }), 200
        else:
            funcionario = Funcionario.query.filter_by(nome=nome).first()

            if not funcionario:
                print(f'ERRO: FUNCIONÁRIO COM NOME "{nome}" NAO ENCONTRADO.')
                return jsonify({
                    'success':False,
                    'msg':f'ERRO: FUNCIONÁRIO: "{nome}" NÃO ENCONTRADO'
                }), 404
        
            data_registro = f"{str(registro.get('dia'))}/{str(registro.get('mes'))}/{str(registro.get('ano'))}"
            tempo_registro = f"{str(registro.get('hora'))}:{str(registro.get('minuto'))}:{str(registro.get('segundo'))}"
            funcao = registro.get('funcao')

            nova_frequencia = Frequencia(
                id_funcionario=funcionario.id_funcionario,
                nome=nome,
                data=data_registro,
                hora=tempo_registro,
                funcao=funcao
            )

            db.session.add(nova_frequencia)
            db.session.commit()

            print('Frequência registrada com sucesso')
            return jsonify({
                "success": True,
                "msg": "Frequência registrada com sucesso"
            }), 200

    except Exception as erro:
        db.session.rollback()

        print('=============================================')
        print(f'ERRO DETECTADO, FUNÇÃO: FREQUÊNCIA')
        print(f'TIPO DO ERRO: {type(erro)}')
        print(f'DESCRIÇÃO: {str(erro)}')
        print('=============================================')

        return jsonify({
            "success": False,
            "msg": "Falha ao registrar a frequência"
        }), 500

        








@app.route('/recuperar-senha', methods=['GET'])
def recuperar():
    try:
        cpf = request.args.get('cpf')

        if not cpf:
            return jsonify({
                "success":False,
                "msg":"CPF é obrigatório para a recuperação. Por favor digite seu cpf"
            }), 400
        
        registro = Funcionario.query.filter_by(cpf=cpf).first()
        print(f'Registro: {registro}')

        if registro is None:
            return jsonify({
                "success":False,
                "msg":"CPF não foi encontrado em nossos registros. Verifique sua conexão"
            }), 404
        else:
            return jsonify({
                "success":True,
                "msg":"Registro localizado. Seu nome de usuário foi preenchido",
                "nome":registro.nome
            }), 200
    except Exception as erro:
        db.session.rollback()

        print('=============================================')
        print(f'ERRO DETECTADO, FUNÇÃO: RECUPERAR SENHA')
        print(f'TIPO DO ERRO: {type(erro)}')
        print(f'DESCRIÇÃO: {str(erro)}')
        print('=============================================')

        return jsonify({
            "success": False,
            "msg": "Erro ao executar a função"
        }), 500







    
    

# aqui uma função importante, pós ela vai ser o referêncial para login, recuperação e consulta;



@app.route('/cadastrar_funcionario', methods=['POST'])
def cadastrar_funcionario():
    try:
        # Pega os dados do corpo da requisição
        dados = request.get_json()

        # Validações mantidas
        if type(dados.get('nome')) is not str or not dados.get('nome').strip():
            return jsonify({
                "success": False,
                "msg": "Campo nome vázio ou tipo de dado inválido"
            }), 400
        
        if type(dados.get('senhaa')) is not str or not dados.get('senhaa').strip():
            return jsonify({
                "success": False,
                "msg": "Campo senha vázio ou tipo de dado inválido"
            }), 400
        
        cpf = dados.get('cpf')
        if type(cpf) is not str:
            return jsonify({
                "success": False,
                "msg": "tipo de dado inválido"
            }), 400

        # Limpeza e validação do CPF
        cpf_limpo = cpf.replace('.','').replace('-','').replace(' ','')
        
        if not cpf_limpo.strip():
            return jsonify({
                "success": False,
                "msg": "CPF não pode ser vazio"
            }), 400
        
        if not cpf_limpo.isdigit():
            return jsonify({
                "success": False,
                "msg": "O CPF deve conter apenas números"
            }), 400
        
        if len(cpf_limpo) != 11:
            return jsonify({
                "success": False,
                "msg": "Quantidade inválida para CPF, digite 11 digitos"
            }), 400
        
        if type(dados.get('funcao')) is not str or not dados.get('funcao').strip():
            return jsonify({
                "success": False,
                "msg": "Campo FUNÇÃO vázio ou tipo de dado inválido"
            }), 400

        # Cria um novo objeto Funcionario com os dados validados
        novo_funcionario = Funcionario(
            nome=dados['nome'],
            senha=dados['senhaa'],
            cpf=cpf_limpo,
            funcao=dados['funcao']
        )
        
        # Adiciona o objeto à sessão do banco de dados
        db.session.add(novo_funcionario)
        
        # Confirma a operação de inserção
        db.session.commit()

        return jsonify({
            "success": True,
            "msg": "Dados processados e guardados com sucesso"
        }), 200

    except Exception as erro:
        # Em caso de erro, desfaz a transação
        db.session.rollback()

        print('=============================================')
        print(f'ERRO DETECTADO, FUNÇÃO: CADASTRAR FUNCIONÁRIO')
        print(f'TIPO DO ERRO: {type(erro)}')
        print(f'DESCRIÇÃO: {str(erro)}')
        print('=============================================')

        return jsonify({
            "success": False,
            "msg": "Erro ao executar a função"
        }), 500









@app.route('/adicionarAtividade', methods=['POST'])
def adicionarAtividade():
    try:
        # Pega os dados do corpo da requisição
        dados = request.get_json()
        
        # As validações foram mantidas, pois são essenciais
        if type(dados.get('tipoDeServico')) is not str:
            return jsonify({
                "success": False,
                "msg": "o Input do tipo de serviço tem que ser do tipo texto"
            }), 400
        
        if type(dados.get('descricao')) is not str or not dados.get('descricao').strip():
            return jsonify({
                "success": False,
                "msg": "o Input descrição tem que ser do tipo TEXT"
            }), 400
        
        if type(dados.get('quem')) is not str or not dados.get('quem').strip():
            return jsonify({
                "success": False,
                "msg": "o Input QUEM tem que ser do tipo TEXT"
            }), 400
        
        if type(dados.get('armazenna')) is not str or not dados.get('armazenna').strip():
            return jsonify({
                "success": False,
                "msg": "o Input armazenna tem que ser do tipo TEXT"
            }), 400
        
        if type(dados.get('empresa')) is not str or not dados.get('empresa').strip():
            return jsonify({
                "success": False,
                "msg": "o Input Empresa tem que ser do tipo TEXT"
            }), 400
        
        if type(dados.get('data')) is not str or not dados.get('data').strip():
            return jsonify({
                "success": False,
                "msg": "o Input Data tem que ser do tipo Text ou convertido para texto"
            }), 400

        # Cria um novo objeto Atividade com os dados validados
        nova_atividade = Atividade(
            tipo_de_servico=dados.get('tipoDeServico'),
            descricao=dados.get('descricao'),
            quem=dados.get('quem'),
            armazenna=dados.get('armazenna'),
            empresa=dados.get('empresa'),
            data=dados.get('data')
        )
        
        # Adiciona e salva o objeto no banco de dados
        db.session.add(nova_atividade)
        db.session.commit()

        return jsonify({
            "success": True,
            # Corrigi a palavra 'success' para 'sucesso'
            "msg": "Função adicionar atividade realizada com sucesso"
        }), 200

    except Exception as erro:
        # Em caso de erro, desfaz a transação para garantir a integridade dos dados
        db.session.rollback()

        print('=============================================')
        print(f'ERRO DETECTADO, FUNÇÃO: ADICIONAR ATIVIDADE')
        print(f'TIPO DO ERRO: {type(erro)}')
        print(f'DESCRIÇÃO: {str(erro)}')
        print('=============================================')

        return jsonify({
            "success": False,
            "msg": "Erro ao executar a função"
        }), 500











@app.route('/excluirFuncionario', methods=['POST'])
def excluirFuncionario():
    try:
        # Pega os dados do corpo da requisição
        dados = request.get_json()
        id_str = dados.get('id')

        # Valida se o ID foi fornecido
        if not id_str:
            return jsonify({
                "success": False,
                "msg": "O ID não foi fornecido."
            }), 400

        try:
            # Tenta converter o ID para um número inteiro
            id_convertido = int(id_str)
        except ValueError:
            # Se a conversão falhar, retorna um erro
            return jsonify({
                "success": False,
                "msg": "ID do funcionário inválido. Deve ser um número inteiro."
            }), 400

        # Busca o funcionário pelo ID. O método .get() é otimizado para chaves primárias.
        funcionario = Funcionario.query.get(id_convertido)

        # Se o funcionário não for encontrado, retorna um erro
        if not funcionario:
            return jsonify({
                "success": False,
                "msg": f"Funcionário com o ID: {id_str} não foi encontrado."
            }), 404
        
        # Se o funcionário for encontrado, o deleta
        db.session.delete(funcionario)
        db.session.commit()

        return jsonify({
            "success": True,
            "msg": "Registro do funcionário localizado e deletado com sucesso."
        }), 200
        
    except Exception as erro:
        # Em caso de erro, desfaz a transação para garantir a integridade dos dados
        db.session.rollback()

        print('=============================================')
        print(f'ERRO DETECTADO, FUNÇÃO: EXCLUIR FUNCIONÁRIO')
        print(f'TIPO DO ERRO: {type(erro)}')
        print(f'DESCRIÇÃO: {str(erro)}')
        print('=============================================')

        return jsonify({
            "success": False,
            "msg": "Erro ao executar a função EXCLUIR FUNCIONÁRIO"
        }), 500








@app.route('/excluiratividade', methods=['POST'])
def excluiratividade():
    try:
        # Pega os dados do corpo da requisição
        dados = request.get_json()
        id_str = dados.get('id_atividade')

        # Valida se o ID foi fornecido
        if not id_str:
            return jsonify({
                "success": False,
                "msg": "O ID não foi fornecido."
            }), 400
        
        try: 
            # Tenta converter o ID para um número inteiro
            id_convertido = int(id_str)
        except ValueError:
            # Se a conversão falhar, retorna um erro
            return jsonify({
                "success": False,
                "msg": "ID da atividade é inválido. Deve ser um número inteiro."
            }), 400
        
        # Busca a atividade pelo ID. O método .get() é otimizado para chaves primárias.
        atividade = Atividade.query.get(id_convertido)

        # Se a atividade não for encontrada, retorna um erro com status 404
        if not atividade:
            return jsonify({
                "success": False,
                "msg": f'Atividade com o ID: {id_str} não encontrada.'
            }), 404
        
        # Se a atividade for encontrada, a deleta
        db.session.delete(atividade)
        db.session.commit()

        return jsonify({
            "success": True,
            "msg": f"Atividade de ID: {id_str} deletada com sucesso."
        }), 200
        
    except Exception as erro:
        # Em caso de erro, desfaz a transação para garantir a integridade dos dados
        db.session.rollback()

        print('=============================================')
        print(f'ERRO DETECTADO, FUNÇÃO: EXCLUIR ATIVIDADE')
        print(f'TIPO DO ERRO: {type(erro)}')
        print(f'DESCRIÇÃO: {str(erro)}')
        print('=============================================')

        return jsonify({
            "success": False,
            "msg": "Erro ao executar a função EXCLUIR ATIVIDADE."
        }), 500







@app.route('/alterarfuncionario', methods=['POST'])
def alterarfuncionario():
    try:
        novos_dados = request.get_json()
        id_str = novos_dados.get('id')

        if not id_str or not str(id_str).strip():
            return jsonify({
                'success':False,
                'msg':"ID não fornecido, por favor insira um valor válido"
            }), 400
        
        try:
            id_int = int(id_str)
        except ValueError:
            return jsonify({
                "success":False,
                "msg":"ID inválido, deve ser um número"
            }), 400
        
        funcionario = Funcionario.query.get(id_int)

        if not funcionario:
            return jsonify({
                "success":False,
                "msg":f'Funcionário de ID: {id_str} não encontrado'
            }), 404
        
        nomenovo = novos_dados.get('nome')
        if nomenovo is not None and isinstance(nomenovo, str) and nomenovo.strip():
            funcionario.nome = nomenovo.strip()

        # Atualiza a senha
        senhanovo = novos_dados.get('senha')
        if senhanovo is not None and isinstance(senhanovo, str) and senhanovo.strip():
            funcionario.senha = senhanovo.strip()

        # Atualiza o CPF
        cpfnovo = novos_dados.get('cpf')
        if cpfnovo is not None and isinstance(cpfnovo, str) and cpfnovo.strip():
            cpf_limpo = cpfnovo.replace('.', '').replace('-', '').replace(' ', '')
            funcionario.cpf = cpf_limpo

        # Atualiza a função
        funcaonovo = novos_dados.get('funcao')
        if funcaonovo is not None and isinstance(funcaonovo, str) and funcaonovo.strip():
            funcionario.funcao = funcaonovo.strip()

        # Confirma as alterações no banco de dados
        db.session.commit()

        return jsonify({
            "success": True,
            "msg": "Funcionário modificado com sucesso."
        }), 200

    except Exception as erro:
        # Em caso de erro, desfaz a transação para garantir a integridade dos dados
        db.session.rollback()

        print('=============================================')
        print(f'ERRO DETECTADO, FUNÇÃO: MODIFICAR FUNCIONÁRIO')
        print(f'TIPO DO ERRO: {type(erro)}')
        print(f'DESCRIÇÃO: {str(erro)}')
        print('=============================================')

        return jsonify({
            "success": False,
            "msg": "Erro ao executar a função MODIFICAR FUNCIONÁRIO"
        }), 500









@app.route('/alterarAtividade', methods=['POST'])
def alterarAtividade():
    try:
        # Pega os dados do corpo da requisição
        novos_dados = request.get_json()
        id_str = novos_dados.get('id_atividade')
        
        # Valida se o ID foi fornecido e se é um número inteiro
        if not id_str or not str(id_str).strip():
            return jsonify({
                "success": False,
                "msg": "ID não fornecido, por favor insira um valor."
            }), 400
        
        try:
            id_int = int(id_str)
        except ValueError:
            return jsonify({
                "success": False,
                "msg": f"ID: {id_str} inválido, deve ser um número inteiro."
            }), 400
        
        # Busca a atividade pelo ID. O método .get() é otimizado para chaves primárias.
        atividade = Atividade.query.get(id_int)
        
        # Se a atividade não for encontrada, retorna um erro com status 404
        if not atividade:
            return jsonify({
                "success": False,
                "msg": f"Atividade com o ID: {id_str} não foi encontrada."
            }), 404
        
        # Lógica de atualização:
        # Pega os novos valores e atualiza os campos se eles não forem nulos ou vazios
        servico_novo = novos_dados.get('servico')
        if servico_novo is not None and isinstance(servico_novo, str) and servico_novo.strip():
            atividade.tipo_de_servico = servico_novo.strip()
            
        descricao_nova = novos_dados.get('descricao')
        if descricao_nova is not None and isinstance(descricao_nova, str) and descricao_nova.strip():
            atividade.descricao = descricao_nova.strip()

        quem_novo = novos_dados.get('quem')
        if quem_novo is not None and isinstance(quem_novo, str) and quem_novo.strip():
            atividade.quem = quem_novo.strip()

        armazenna_novo = novos_dados.get('armazenna')
        if armazenna_novo is not None and isinstance(armazenna_novo, str) and armazenna_novo.strip():
            atividade.armazenna = armazenna_novo.strip()

        empresa_nova = novos_dados.get('empresa')
        if empresa_nova is not None and isinstance(empresa_nova, str) and empresa_nova.strip():
            atividade.empresa = empresa_nova.strip()

        data_nova = novos_dados.get('data')
        if data_nova is not None and isinstance(data_nova, str) and data_nova.strip():
            atividade.data = data_nova.strip()

        status_novo = novos_dados.get('status')
        if status_novo is not None and isinstance(status_novo, str) and status_novo.strip():
            atividade.status = status_novo.strip()

        # Confirma as alterações no banco de dados
        db.session.commit()

        return jsonify({
            "success": True,
            "msg": f"Atividade de ID: {id_str} modificada com sucesso."
        }), 200

    except Exception as erro:
        # Em caso de erro, desfaz a transação para garantir a integridade dos dados
        db.session.rollback()

        print('=============================================')
        print(f'ERRO DETECTADO, FUNÇÃO: MODIFICAR ATIVIDADE')
        print(f'TIPO DO ERRO: {type(erro)}')
        print(f'DESCRIÇÃO: {str(erro)}')
        print('=============================================')

        return jsonify({
            "success": False,
            "msg": "Erro ao executar a função MODIFICAR ATIVIDADE."
        }), 500











@app.route('/ordenarAtividades', methods=['POST'])
def ordenarAtividades():
    try:
        dados = request.get_json()
        ordenar_por = dados.get('ordenar_por', 'id_atividade')
        direcao = dados.get('direcao', 'asc')  # Pega a direção da ordenação, com 'asc' como padrão

        print(f'Dados: {dados}; Ordenar por: {ordenar_por}; Direção: {direcao}')

        # Dicionário que mapeia o nome da coluna para o atributo do modelo
        mapeamento_colunas = {
            'id_atividade': Atividade.id_atividade,
            'tipo_de_servico': Atividade.tipo_de_servico,
            'descricao': Atividade.descricao,
            'quem': Atividade.quem,
            'armazenna': Atividade.armazenna,
            'empresa': Atividade.empresa,
            'data': Atividade.data,
            'status': Atividade.status,
        }

        # Pega o atributo do modelo correspondente ao critério de ordenação
        # Se o critério não for válido, ordena por 'id_atividade' como padrão.
        coluna_ordenacao = mapeamento_colunas.get(ordenar_por, Atividade.id_atividade)

        # Aplica a ordenação ascendente ou descendente
        if direcao.lower() == 'desc':
            query_ordenada = Atividade.query.order_by(desc(coluna_ordenacao)).all()
        else:
            query_ordenada = Atividade.query.order_by(asc(coluna_ordenacao)).all()

        lista_json = []

        # Itera sobre os objetos do Flask-SQLAlchemy e os converte para dicionários
        for atividade in query_ordenada:
            dicionario = {
                'id_atividade': atividade.id_atividade,
                'tipo_de_servico': atividade.tipo_de_servico,
                'descricao': atividade.descricao,
                'quem': atividade.quem,
                'armazenna': atividade.armazenna,
                'empresa': atividade.empresa,
                'data': atividade.data,
                'status': atividade.status
            }
            lista_json.append(dicionario)

        print('Comunicação realizada com a API')
        return jsonify({
            "success": True,
            "msg": f"Atividades ordenadas por: {ordenar_por}",
            "lista": lista_json
        }), 200

    except Exception as erro:
        # Em caso de erro, desfaz a transação para garantir a integridade dos dados
        db.session.rollback()

        print('=============================================')
        print(f'ERRO DETECTADO, FUNÇÃO: ORDENAR ATIVIDADE')
        print(f'TIPO DO ERRO: {type(erro)}')
        print(f'DESCRIÇÃO: {str(erro)}')
        print('=============================================')

        return jsonify({
            "success": False,
            "msg": f"Erro ao executar a função ORDENAR ATIVIDADE; DESCRIÇÃO: {str(erro)}; TYPE: {type(erro)}"
        }), 500












@app.route('/ordenarfuncionarios', methods=['POST'])
def ordenarfuncionarios():
    try:
        dados = request.get_json()
        ordenar_por = dados.get('ordenar_por')
        direcao = dados.get('direcao', 'asc')  # Pega a direção da ordenação, com 'asc' como padrão

        print(f'Dados: {dados}; Ordenar por: {ordenar_por}; Direção: {direcao}')

        # Dicionário que mapeia o nome da coluna para o atributo do modelo
        mapeamento_colunas = {
            'id_funcionario': Funcionario.id_funcionario,
            'nome': Funcionario.nome,
            'senha': Funcionario.senha,
            'cpf': Funcionario.cpf,
            'funcao': Funcionario.funcao,
        }

        # Pega o atributo do modelo correspondente ao critério de ordenação
        # Se o critério não for válido, ordena por 'id_funcionario' como padrão.
        coluna_ordenacao = mapeamento_colunas.get(ordenar_por, Funcionario.id_funcionario)

        # Aplica a ordenação ascendente ou descendente
        if direcao.lower() == 'desc':
            query_ordenada = Funcionario.query.order_by(desc(coluna_ordenacao)).all()
        else:
            query_ordenada = Funcionario.query.order_by(asc(coluna_ordenacao)).all()
            
        lista_json = []

        # Itera sobre os objetos do Flask-SQLAlchemy e os converte para dicionários
        for funcionario in query_ordenada:
            dicionario = {
                'id_funcionario': funcionario.id_funcionario,
                'nome': funcionario.nome,
                'senha': funcionario.senha,
                'cpf': funcionario.cpf,
                'funcao': funcionario.funcao,
            }
            lista_json.append(dicionario)

        print('Comunicação realizada com a API')
        return jsonify({
            "success": True,
            "msg": f"Funcionários ordenados por: {ordenar_por}",
            "lista": lista_json
        }), 200

    except Exception as erro:
        # Em caso de erro, desfaz a transação para garantir a integridade dos dados
        db.session.rollback()

        print('=============================================')
        print(f'ERRO DETECTADO, FUNÇÃO: ORDENAR FUNCIONÁRIOS')
        print(f'TIPO DO ERRO: {type(erro)}')
        print(f'DESCRIÇÃO: {str(erro)}')
        print('=============================================')

        return jsonify({
            "success": False,
            "msg": "Erro ao executar a função ORDENAR FUNCIONÁRIOS"
        }), 500







@app.route('/mostrar_atividades', methods=['POST'])
def mostrar_atividades():
    try:
        dados = request.get_json()
        tipo_servico_solicitado = dados.get('msg')
        
        # Mapeia as mensagens do JSON para os valores do banco de dados
        mapeamento_servicos = {
            'atividades de elétrica': 'ELÉTRICA',
            'atividades de mecanica': 'MECÂNICA',
            'atividades de pintura': 'PINTURA',
            'atividades de telhado': 'TELHADO'
        }
        
        # Pega o valor correto do serviço. Se a mensagem não for válida, retorna None.
        servico = mapeamento_servicos.get(tipo_servico_solicitado)

        # Se a mensagem de serviço não for encontrada no mapeamento, retorna um erro
        if not servico:
            return jsonify({
                "success": False,
                "msg": "Erro ao identificar qual área da atividade pegar. Mensagem inválida."
            }), 404
        
        # Busca as atividades no banco de dados usando o Flask-SQLAlchemy
        # Filtra pelo tipo de serviço e ordena por id_atividade
        atividades = Atividade.query.filter_by(tipo_de_servico=servico).order_by(asc(Atividade.id_atividade)).all()

        # Converte os objetos do Flask-SQLAlchemy para uma lista de dicionários
        lista_json = []
        for atividade in atividades:
            lista_json.append({
                'id_atividade': atividade.id_atividade,
                'tipo_de_servico': atividade.tipo_de_servico,
                'descricao': atividade.descricao,
                'quem': atividade.quem,
                'armazenna': atividade.armazenna,
                'empresa': atividade.empresa,
                'data': atividade.data,
                'status': atividade.status
            })

        return jsonify({
            "success": True,
            "msg": f"Atividades de '{servico}' localizadas com sucesso.",
            "lista": lista_json
        }), 200
        
    except Exception as erro:
        db.session.rollback()

        print('=============================================')
        print(f'ERRO DETECTADO, FUNÇÃO: MOSTRAR ATIVIDADES')
        print(f'TIPO DO ERRO: {type(erro)}')
        print(f'DESCRIÇÃO: {str(erro)}')
        print('=============================================')

        return jsonify({
            "success": False,
            "msg": "Erro ao executar a função MOSTRAR ATIVIDADES."
        }), 500












# rota que vai receber os dados la da tela de login
@app.route('/receber_dados', methods=['POST'])
def receber_dados():
    try:
        dados_recebidos = request.get_json()
        nome = dados_recebidos.get('nome')
        senha = dados_recebidos.get('senhar')
        
        # --- ATENÇÃO: INSEGURANÇA GRAVE ---
        # A lógica abaixo é um acesso emergencial com credenciais fixas.
        # Isso representa um grande risco de segurança e deve ser substituído por um
        # mecanismo de autenticação seguro.
        if nome == 'none' and senha == 'none':
            return jsonify({
                "success": True,
                "msg": "ACESSO EMERGÊNCIAL",
                "texto": "001",
                "funcao": "adm"
            }), 200
        # --- FIM DO BLOCO INSEGURO ---

        # Usa o Flask-SQLAlchemy para buscar o funcionário de forma segura
        # A busca por `first()` retorna o primeiro resultado ou None se não encontrar
        funcionario = Funcionario.query.filter_by(nome=nome, senha=senha).first()
        
        # Se o funcionário não for encontrado, retorna uma falha de autenticação
        if not funcionario:
            return jsonify({
                "success": False,
                "msg": "Dados inválidos ou campo vazio, tente novamente."
            }), 401
        
        # Se o funcionário for encontrado, retorna os dados de sucesso
        funcao = funcionario.funcao
        return jsonify({
            "success": True,
            "msg": "LOGIN CONCEDIDO",
            "texto": "001",
            "funcao": funcao
        }), 200
        
    except Exception as erro:
        # Em caso de erro, desfaz a transação para garantir a integridade dos dados
        # A função rollback() é importante para garantir que nenhuma transação incompleta persista
        db.session.rollback()

        print('=============================================')
        print(f'ERRO DETECTADO, FUNÇÃO: RECEBER DADOS')
        print(f'TIPO DO ERRO: {type(erro)}')
        print(f'DESCRIÇÃO: {str(erro)}')
        print('=============================================')

        return jsonify({
            "success": False,
            "msg": "Erro ao processar os dados"
        }), 500


    


@app.route('/tela02')
def tela02():
    return render_template('tela02.html')


@app.route('/pintura')
def pintura():
    return render_template('pintura.html')


@app.route('/eletrica')
def eletrica():
    return render_template('eletrica.html')


@app.route('/mecanica')
def mecanica():
    return render_template('mecanica.html')


@app.route('/telhado')
def telhado():
    return render_template('telhado.html')


@app.route('/adm')
def adm():
    return render_template('adm.html')



# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
#     app.run(debug=False)

if __name__ == '__main__':
    app.run(debug=True)

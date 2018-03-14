#!/usr/bin/env python3
# encoding: utf-8
"""
Este módulo é parte integrante da aplicação Promais Service, desenvolvida por
Victor Domingos e distribuída sob os termos da licença Creative Commons
Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
"""
import os
import pprint
import random
import string

from getpass import getpass
from datetime import datetime

from passlib.hash import pbkdf2_sha256

from local_db import db_models, db_base
from local_db import db_main as db

from global_setup import LOCAL_DATABASE_PATH
from misc.constants import ESTADOS, ENTREGUE, PRIORIDADES, RESULTADOS
from misc.misc_funcs import check_and_normalize_phone_number, obfuscate_text

def delete_database():
    print("  - A apagar as tabelas existentes.")
    s, engine = db.iniciar_sessao_db()
    db_base.Base.metadata.drop_all(engine)
    s.commit()
    s.close()


def vacuum_db():
    print('  - A "aspirar" a base de dados.')
    import sqlalchemy
    engine = sqlalchemy.create_engine('sqlite:///' + LOCAL_DATABASE_PATH)
    con = engine.raw_connection()
    cursor = con.cursor()
    command = "VACUUM"
    cursor.execute(command)
    con.commit()
    cursor.close()


def init_database():
    print("  - A (re)criar as tabelas necessárias.")
    s, engine = db.iniciar_sessao_db()
    db_base.Base.metadata.create_all(engine)
    s.commit()
    s.close()


# ----------------------------------------------------------------------------------------
# Just a bunch of experiences to get the hang of SQLalchemy while developing the models...
# ----------------------------------------------------------------------------------------

def test_populate(num_lojas=1, admin_password_hash="", num_utilizadores=1, num_contactos=1, num_artigos=1, num_reparacoes=1):
    print("\nA inserir dados de exemplo na base de dados.")

    print("  - A criar o grupo de administradores...")
    db.create_store(nome=f"The System Administration Guys")

    print("  - A criar um administrador para a base de dados...")
    db.create_user(username="npk", email="admin@networkprojectforknowledge.org",
                   password=admin_password_hash, loja_id=1)


    for i in range(num_lojas):
        print(f"{'  - A inserir lojas...'.ljust(55)}{i+1:7}", end="\r")
        db.create_store(nome=f"That Great NPK Store #{str(i)}")

    print("")


    s, _ = db.iniciar_sessao_db()
    lojas_q = s.query(db_models.Loja)
    lojas = lojas_q.all()

    for i in range(num_utilizadores):
        print(f"{'  - A inserir utilizadores...'.ljust(55)}{i+1:7}", end="\r")
        lojinha = lojas[i % 2]
        db.create_user(username="utilizador" + str(i), email="test@networkprojectforknowledge.org" + str(i), password=pbkdf2_sha256.hash("abc1234567"), loja_id=lojinha.id)


    s, _ = db.iniciar_sessao_db()
    print("")
    utilizadores = s.query(db_models.User).all()
    nomes = ("José", "Rita", "Shawn", "Francelina", "Eufrazina", "Eleutério", "Joana Manuela", "Manuel", "Maria", "Guilhermina", "Estêvão", "Joaninha", "Apólito", "John", "Loja X")
    apelidos = ("Laranja", "Bonito", "Santiago", "de Malva e Cunha", "Azeredo", "Starck", "Brückner", "Apolinário Gomes Fernandes", "Carvalho", "Rodrigues", "Ló")
    empresas = ("", "NPK", "NPK - Network project for Knowledge", "Aquela Empresa Faltástica, S.A.", "", "")
    telefones = ("222000000", "960000000", "+351210000000")
    emails = ("test", "info", "npk", "theworldisavampire", "florzinha98", "josefloresmanuel", "mariazinha1978")
    dominios = ("networkprojectforknowledge.org", "baratatonta2001.com.br", "thegreatnpkdomain.com", "zbxvsga.pt", "ihopethisdomaindoesnotexist.net")
    is_cliente = (True, False)
    is_fornecedor = (*20*(False,), True)

    from random import choice
    for i in range(num_contactos):
        print(f"{'  - A inserir contactos (clientes e fornecedores)...'.ljust(55)}{i+1:7}", end="\r")
        forn = choice(is_fornecedor)

        if forn:
            cli = choice(is_cliente)
        else:
            cli = True

        if i == 0:
            atualizado_por_utilizador = None
        else:
            atualizado_por_utilizador = choice(utilizadores)

        contacto = db_models.Contact(
            nome=f"{choice(nomes)} {choice(apelidos)}",
            empresa=choice(empresas),
            telefone= check_and_normalize_phone_number(choice(telefones)),
            telemovel = check_and_normalize_phone_number(choice(telefones)),
            telefone_empresa = check_and_normalize_phone_number(choice(telefones)),
            email = choice(emails) + "@" + choice(dominios),
            morada = "Rua da Santa Paciência Que Nos Acuda Em Dias Daqueles\nEdifício Especial XXI, porta 789, 3º Esquerdo Trás",
            cod_postal = "4700-000",
            localidade = "Braga",
            pais = "Portugal",
            nif = "999999990",
            notas = "Apontamentos adicionais sobre este contacto...",
            is_cliente = bool(cli),
            is_fornecedor = bool(forn),
            criado_por_utilizador = choice(utilizadores),
            atualizado_por_utilizador = atualizado_por_utilizador)
        s.add(contacto)

    #s.commit()


    print("")
    artigos = ("Artigo Muito Jeitoso (Early 2015)", "Outro Artigo Bem Jeitoso",
        "Smartphone Daqueles Bons", "Computador do modelo ABCD",
        "Coisa que não funciona devidamente", "Coisa que devia funcionar melhor")

    for i in range(num_artigos):
        print(f"{'  - A inserir artigos...'.ljust(55)}{i+1:7}", end="\r")

        artigo = db_models.Product(descr_product=choice(artigos), part_number="NPKPN662"+str(i)+"ZQ"+str(i))
        s.add(artigo)

    #s.commit()

    print("")
    contactos = s.query(db_models.Contact).all()
    num_contactos = s.query(db_models.Contact).count()
    artigos = s.query(db_models.Product).all()
    num_artigos = s.query(db_models.Product).count()
    utilizadores = s.query(db_models.User).all()
    num_utilizadores = s.query(db_models.User).count()
    servicos = ("Substituição de ecrã", "Bateria não carrega",
        "Formatar disco e reinstalar sistema operativo",
        "Substituição ao abrigo da garantia")

    for i in range(num_reparacoes):
        print(f"{'  - A inserir reparações...'.ljust(55)}{i+1:7}", end="\r")
        if (i%2 == 1) or (i%3 == 0) or (i%10 == 0) or i<1000 or i>1150:
            estado = ENTREGUE
        else:
            estado = choice(list(ESTADOS.keys()))
        reparacao = db_models.Repair(
            cliente = contactos[i%num_contactos],
            product = artigos[i%num_artigos],
            sn = ''.join(random.choices(string.ascii_uppercase + string.digits, k=21)),
            fornecedor = contactos[(i+5)%num_contactos],
            estado_artigo = 1,
            obs_estado = "Marcas de acidente, com amolgadelas e vidro partido",
            is_garantia = 0,
            data_compra = datetime(2017,1,31),
            num_fatura = ''.join(random.choices(string.digits, k=12)),
            loja_compra = "NPK Store",
            descr_servico = choice(servicos),
            avaria_reprod_loja = True,
            requer_copia_seg = 0,
            is_find_my_ativo = 1,
            senha = obfuscate_text("123456"),
            acessorios_entregues = "Bolsa da marca NPK Accessories",
            notas = "",
            local_reparacao = contactos[i%2],
            estado_reparacao = estado,
            fatura_fornecedor = "FC12341"+''.join(random.choices(string.ascii_uppercase + string.digits, k=5)),
            nar_autorizacao_rep = random.randint(1,999999),
            data_fatura_fornecedor = datetime(2017,1,31),
            num_guia_rececao = random.randint(1,99999),
            data_guia_rececao = datetime(2017,1,31),
            cod_resultado_reparacao = choice(list(RESULTADOS.keys())),
            descr_detalhe_reparacao = "Foi substituído em garantia o neurónio avariado",
            novo_sn_artigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=21)),
            notas_entrega = "Entregue a José Manuel da Silva Curioso",

            utilizador_entrega = utilizadores[(i+5)%num_utilizadores],
            prioridade = choice(list(PRIORIDADES.items())),
            data_entrega = datetime(2017,1,31),
            num_quebra_stock = "1234",
            is_stock = 0,
            modo_entrega = 0,
            cliente_pagou_portes = 0,
            reincidencia_processo_id = 123,
            morada_entrega = "",

            criado_por_utilizador = utilizadores[i%num_utilizadores])
        s.add(reparacao)

    #s.commit()


    print("")
    reparacoes = s.query(db_models.Repair).all()
    utilizadores = s.query(db_models.User).all()
    count = 0
    rep = reparacoes[1]
    for rep in reparacoes:
        print(f"{'  - A inserir eventos...'.ljust(55)}{count+1:7}", end="\r")
        count +=1
        #print("event in rep", rep)
        # create parent, append a child via association
        evento1 = db_models.Event(
            repair_id = rep.id,
            descricao = "Cliente enviou por email a fatura para anexar ao processo de garantia.",
            criado_por_utilizador = choice(utilizadores))

        link = db_models.UtilizadorNotificadoPorEvento_link(
            is_visible=choice([False, True]),
            is_open=choice([True, False]))

        link.user = choice(utilizadores)
        evento1.utilizadores.append(link)
        s.add(evento1)

        textos = ("Centro técnico pediu para questionar cliente sobre algo importante.",
                  "Falta enviar a fatura para garantia.")
        if count % 2 == 0:
            #print("if rep event")
            evento2 = db_models.Event(
                repair_id = rep.id,
                descricao = choice(textos),
                criado_por_utilizador = utilizadores[0])

            link2 = db_models.UtilizadorNotificadoPorEvento_link(
                is_visible=choice([True, False]),
                is_open=choice([False, True]))
            link2.user = utilizadores[0]
            evento2.utilizadores.append(link2)
            s.add(evento2)
            if count >=50:
                break

    s.commit()


def print_database():
    s, _ = db.iniciar_sessao_db()

    lojas = s.query(db_models.Loja).all()
    utilizadores = s.query(db_models.User).all()
    contactos = s.query(db_models.Contact).all()
    artigos = s.query(db_models.Product).all()
    reparacoes = s.query(db_models.Repair).all()
    eventos = s.query(db_models.Event).all()
    eventos_visiveis = s.query(db_models.UtilizadorNotificadoPorEvento_link).filter_by(is_visible=1, user=utilizadores[2])

    print("\n========================\n          LOJAS\n========================")
    for lojinha in lojas:
        print(f"\nA loja {lojinha.nome}, com o ID {lojinha.id}, tem os seguintes utilizadores:)")
        pprint.pprint([(u.id, u.nome) for u in lojinha.users])


    print("\n==============================\n         UTILIZADORES\n==============================")
    for utilizador in utilizadores:
        print(f"\nO utilizador {utilizador.nome} tem o ID {utilizador.id} pertence à loja: {utilizador.loja_id} ({utilizador.loja.nome})")


    print("\n==============================\n          CONTACTOS\n==============================")
    for contacto in contactos:
        print(contacto)
        print("\nReparações como cliente:")
        pprint.pprint([(rep.id, rep.product.descr_product, rep.cliente.nome) for rep in contacto.reparacoes_como_cliente])
        print("\nReparações como fornecedor:")
        pprint.pprint([(rep.id, rep.product.descr_product, rep.cliente.nome) for rep in contacto.reparacoes_como_fornecedor])


    print("\n========================\n           ARTIGOS\n========================")
    for artigo in artigos:
        pprint.pprint(artigo)


    print("\n========================\n           REPARAÇÕES\n========================")
    for reparacao in reparacoes:
        pprint.pprint(reparacao)

    print("\n========================\n           EVENTOS\n========================")
    for evento in eventos:
        pprint.pprint(evento)

    print("\n========================\n           EVENTOS Visíveis\n========================")
    for link in eventos_visiveis:
        pprint.pprint(link.event)


if __name__ == "__main__":
    # Testing...

    try:
        db_filesize = os.path.getsize(os.path.expanduser(LOCAL_DATABASE_PATH)) >> 10
        print(f"\nEncontrado ficheiro de dase de dados (tamanho atual: {db_filesize/1024:.1f}MB)")
    except:
        print("\nNão foi encontrado nenhum ficheiro de base de dados. A criar um novo.")

    print("\nA preparar o ficheiro de base de dados...")
    try:
        delete_database()
        vacuum_db()
        init_database()
    except:
        print("Não foi possível inicializar a base de dados na localização indicada. É possível "
              "que a seguinte pasta não exista ou não tenha as permissões necessárias:")
        print(LOCAL_DATABASE_PATH)
        exit()

    admin_password = getpass("\nPor favor introduza a senha para o administrador (npk): ")
    password_hash = pbkdf2_sha256.using(salt_size=8).hash(admin_password)

    num_lojas = 2

    utilizadores = num_lojas * 8
    contactos = num_lojas * 850
    artigos = num_lojas * 600
    reps = num_lojas * 3000

    test_populate(num_lojas=num_lojas,
                  admin_password_hash = password_hash,
                  num_utilizadores=utilizadores,
                  num_contactos=contactos,
                  num_artigos=artigos,
                  num_reparacoes=int(reps))

    db_filesize = os.path.getsize(os.path.expanduser(LOCAL_DATABASE_PATH)) >> 10
    print(f"\n\nOperação terminada.\nTamanho atual da base de dados: {db_filesize/1024:.1f}MB")

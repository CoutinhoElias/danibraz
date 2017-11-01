# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-10-29 13:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_key', models.CharField(db_index=True, max_length=40, verbose_name='Chave do Carrinho')),
                ('product', models.CharField(choices=[('ABEV3', 'AMBEV S/A'), ('BBAS3', 'BRASIL'), ('BBDC3', 'BRADESCO 3'), ('BBDC4', 'BRADESCO 4'), ('BBSE3', 'BBSEGURIDADE'), ('BRAP4', 'BRADESPAR'), ('BRFS3', 'BRF SA'), ('BRKM5', 'BRASKEM'), ('BRML3', 'BR MALLS PAR'), ('BVMF3', 'BMFBOVESPA'), ('CCRO3', 'CCR SA'), ('CIEL3', 'CIELO'), ('CMIG4', 'CEMIG'), ('CSAN3', 'COSAN'), ('CSNA3', 'SID NACIONAL'), ('ECOR3', 'ECORODOVIAS'), ('ELET3', 'ELETROBRAS'), ('EMBR3', 'EMBRAER'), ('EQTL3', 'EQUATORIAL'), ('ESTC3', 'ESTACIO PART'), ('FIBR3', 'FIBRIA'), ('GGBR4', 'GERDAU'), ('GOAU4', 'GERDAU MET'), ('HYPE3', 'HYPERMARCAS'), ('ITSA4', 'ITAUSA'), ('ITUB4', 'ITAUUNIBANCO'), ('JBSS3', 'JBS'), ('KLBN11', 'KLABIN S/A'), ('KROT3', 'KROTON'), ('LAME4', 'LOJAS AMERIC'), ('LREN3', 'LOJAS RENNER'), ('MRVE3', 'MRV'), ('MULT3', 'MULTIPLAN'), ('NATU3', 'NATURA'), ('PCAR4', 'P.ACUCAR-CBD'), ('PETR3', 'PETROBRAS'), ('PETR4', 'PETROBRAS'), ('QUAL3', 'QUALICORP'), ('RADL3', 'RAIADROGASIL'), ('RAIL3', 'RUMO S.A.'), ('RENT3', 'LOCALIZA'), ('SANB11', 'SANTANDER BR'), ('SBSP3', 'SABESP'), ('SUZB5', 'SUZANO PAPEL'), ('TAEE11', 'TAESA'), ('UGPA3', 'ULTRAPAR'), ('USIM5', 'USIMINAS'), ('VALE3', 'VALE'), ('VIVT4', 'TELEF BRASIL'), ('WEGE3', 'WEG')], max_length=100, verbose_name='Papel')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Quantidade')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Preço')),
            ],
            options={
                'verbose_name': 'Item do Carrinho',
                'verbose_name_plural': 'Itens dos Carrinhos',
            },
        ),
        migrations.CreateModel(
            name='Lancamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(verbose_name='Data')),
                ('papel', models.CharField(choices=[('ABEV3', 'AMBEV S/A'), ('BBAS3', 'BRASIL'), ('BBDC3', 'BRADESCO 3'), ('BBDC4', 'BRADESCO 4'), ('BBSE3', 'BBSEGURIDADE'), ('BRAP4', 'BRADESPAR'), ('BRFS3', 'BRF SA'), ('BRKM5', 'BRASKEM'), ('BRML3', 'BR MALLS PAR'), ('BVMF3', 'BMFBOVESPA'), ('CCRO3', 'CCR SA'), ('CIEL3', 'CIELO'), ('CMIG4', 'CEMIG'), ('CSAN3', 'COSAN'), ('CSNA3', 'SID NACIONAL'), ('ECOR3', 'ECORODOVIAS'), ('ELET3', 'ELETROBRAS'), ('EMBR3', 'EMBRAER'), ('EQTL3', 'EQUATORIAL'), ('ESTC3', 'ESTACIO PART'), ('FIBR3', 'FIBRIA'), ('GGBR4', 'GERDAU'), ('GOAU4', 'GERDAU MET'), ('HYPE3', 'HYPERMARCAS'), ('ITSA4', 'ITAUSA'), ('ITUB4', 'ITAUUNIBANCO'), ('JBSS3', 'JBS'), ('KLBN11', 'KLABIN S/A'), ('KROT3', 'KROTON'), ('LAME4', 'LOJAS AMERIC'), ('LREN3', 'LOJAS RENNER'), ('MRVE3', 'MRV'), ('MULT3', 'MULTIPLAN'), ('NATU3', 'NATURA'), ('PCAR4', 'P.ACUCAR-CBD'), ('PETR3', 'PETROBRAS'), ('PETR4', 'PETROBRAS'), ('QUAL3', 'QUALICORP'), ('RADL3', 'RAIADROGASIL'), ('RAIL3', 'RUMO S.A.'), ('RENT3', 'LOCALIZA'), ('SANB11', 'SANTANDER BR'), ('SBSP3', 'SABESP'), ('SUZB5', 'SUZANO PAPEL'), ('TAEE11', 'TAESA'), ('UGPA3', 'ULTRAPAR'), ('USIM5', 'USIMINAS'), ('VALE3', 'VALE'), ('VIVT4', 'TELEF BRASIL'), ('WEGE3', 'WEG')], max_length=100, verbose_name='Papel')),
                ('operacao', models.CharField(choices=[('C', 'COMPRA'), ('V', 'VENDA'), ('D', 'DIVIDENDOS'), ('S', 'SPLIT')], max_length=100, verbose_name='Operação')),
                ('quantidade', models.PositiveIntegerField(default=1, verbose_name='Quantidade')),
            ],
            options={
                'verbose_name': 'lançamento',
                'verbose_name_plural': 'lançamentos',
            },
        ),
    ]

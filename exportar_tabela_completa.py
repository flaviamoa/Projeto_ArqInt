#!/usr/bin/env python

from collections import defaultdict
import pybgpstream
import csv
from datetime import datetime


stream = pybgpstream.BGPStream(
    # Consider this time interval:
    # Sat, 01 Aug 2015 7:50:00 GMT -  08:10:00 GMT
    from_time="2023-01-01 00:00:00", until_time="2023-01-01 00:20:00",
    collectors=["rrc15"],
    record_type="ribs",
)

# Abra o arquivo CSV para escrever os dados da tabela de roteamento completa
with open("tabela_roteamento_completa.csv", "w") as csv_file:
    writer = csv.writer(csv_file)

    # Escreva o cabecalho do CSV
    writer.writerow(["Prefixo","Nexthop","as-path","Origem Prefixo"], )

    # <prefix, origin-ASns-set > dictionary
    prefix_origin = defaultdict(set)

    # Itere sobre as atualizacoes de roteamento
    for rec in stream.records():
        for elem in rec:
            if elem.type == "R":

                pfx = elem.fields["prefix"]
                # Get the list of ASes in the AS path
                ases = elem.fields["as-path"].split(" ")
                # Get the next-hop
                nxt_hop = elem.fields["next-hop"]

                if len(ases) > 0:
                    # Get the origin ASn (rightmost)
                    origin = ases[-1]
                    # Insert the origin ASn in the set of
                    # origins for the prefix
                    prefix_origin[pfx].add(origin)
    # Print the list of MOAS prefix and their origin ASns
    for pfx in prefix_origin:
        if len(prefix_origin[pfx]) > 1:
            print((pfx, ",".join(prefix_origin[pfx])))        
            #if elem.type == "R" and elem.fields["valid"]:
            # Escreva os dados da atualizacao no CSV
            writer.writerow([pfx, nxt_hop,ases,prefix_origin[pfx]])

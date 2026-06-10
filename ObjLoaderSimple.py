# ==========================================================
# ObjLoaderSimple.py
# ==========================================================
#
# Loader simples de arquivos .OBJ
#
# O formato OBJ é um formato de modelos 3D
# muito utilizado em computação gráfica.
#
# Ele armazena:
#
# - vértices (v)
# - coordenadas de textura (vt)
# - normais (vn)
# - faces (f)
#
# Neste loader iremos utilizar apenas:
#
# - v  = posição dos vértices
# - vt = coordenadas UV da textura
# - f  = faces do objeto
#
# O objetivo deste código é:
#
# 1) Ler arquivo .OBJ
# 2) Extrair vértices e UVs
# 3) Converter faces em triângulos
# 4) Montar buffer final para OpenGL
#
# ==========================================================

import numpy as np


class ObjLoaderSimple:


    # ======================================================
    # MÉTODO ESTÁTICO
    # ======================================================
    #
    # staticmethod:
    #
    # permite chamar:
    #
    # ObjLoaderSimple.load_obj(...)
    #
    # sem precisar criar um objeto da classe.
    #
    # ======================================================

    @staticmethod
    def load_obj(filename):


        # ==================================================
        # LISTAS PRINCIPAIS
        # ==================================================
        #
        # vertices:
        # armazena posições x y z
        #
        # textures:
        # armazena coordenadas UV
        #
        # faces:
        # armazena índices das faces
        # ==================================================

        vertices = []

        textures = []

        faces = []


        # ==================================================
        # ABRE ARQUIVO OBJ
        # ==================================================
        #
        # "r" = read (leitura)
        #
        # O arquivo será lido linha por linha.
        # ==================================================

        with open(filename, "r") as file:


            # ==================================================
            # LOOP LINHAS DO OBJ
            # ==================================================

            for line in file:


                # ==================================================
                # SPLIT
                # ==================================================
                #
                # divide a linha usando espaços.
                #
                # Exemplo:
                #
                # "v 1.0 2.0 3.0"
                #
                # vira:
                #
                # ["v", "1.0", "2.0", "3.0"]
                # ==================================================

                values = line.split()


                # ==================================================
                # IGNORA LINHAS VAZIAS
                # ==================================================

                if len(values) == 0:

                    continue


                # ======================================================
                # VÉRTICES
                # ======================================================
                #
                # linhas iniciadas com:
                #
                # v
                #
                # representam vértices do modelo.
                #
                # Exemplo:
                #
                # v 1.0 2.0 3.0
                #
                # x = 1.0
                # y = 2.0
                # z = 3.0
                # ======================================================

                if values[0] == "v":


                    # ==================================================
                    # CONVERTE STRINGS PARA FLOAT
                    # ==================================================

                    vertex = [
                        float(values[1]),
                        float(values[2]),
                        float(values[3])
                    ]


                    # ==================================================
                    # ADICIONA VÉRTICE NA LISTA
                    # ==================================================

                    vertices.append(vertex)


                # ======================================================
                # UV (TEXTURA)
                # ======================================================
                #
                # linhas iniciadas com:
                #
                # vt
                #
                # representam coordenadas UV
                # da textura.
                #
                # U = horizontal textura
                # V = vertical textura
                #
                # Exemplo:
                #
                # vt 0.5 1.0
                # ======================================================

                elif values[0] == "vt":


                    # ==================================================
                    # CONVERTE UV PARA FLOAT
                    # ==================================================

                    texcoord = [
                        float(values[1]),
                        float(values[2])
                    ]


                    # ==================================================
                    # ADICIONA UV NA LISTA
                    # ==================================================

                    textures.append(texcoord)


                # ======================================================
                # FACES
                # ======================================================
                #
                # linhas iniciadas com:
                #
                # f
                #
                # representam as faces do objeto.
                #
                # Exemplo:
                #
                # f 1/1 2/2 3/3
                #
                # significa:
                #
                # vértice 1 usa UV 1
                # vértice 2 usa UV 2
                # vértice 3 usa UV 3
                #
                # ======================================================

                elif values[0] == "f":


                    # ==================================================
                    # LISTA TEMPORÁRIA DA FACE
                    # ==================================================

                    face = []


                    # ==================================================
                    # PERCORRE VÉRTICES DA FACE
                    # ==================================================

                    for v in values[1:]:


                        # ==================================================
                        # SPLIT "/"
                        # ==================================================
                        #
                        # Exemplo:
                        #
                        # 5/2/1
                        #
                        # vira:
                        #
                        # ["5","2","1"]
                        #
                        # OBJ normalmente usa:
                        #
                        # posição/textura/normal
                        # ==================================================

                        vals = v.split('/')


                        # ==================================================
                        # ÍNDICE DO VÉRTICE
                        # ==================================================
                        #
                        # OBJ começa em 1
                        #
                        # Python começa em 0
                        #
                        # por isso:
                        #
                        # -1
                        # ==================================================

                        v_idx = int(vals[0]) - 1


                        # ==================================================
                        # ÍNDICE UV
                        # ==================================================

                        vt_idx = int(vals[1]) - 1


                        # ==================================================
                        # SALVA TUPLA
                        # ==================================================
                        #
                        # (índice vértice, índice UV)
                        # ==================================================

                        face.append((v_idx, vt_idx))


                    # ==================================================
                    # TRIANGULIZAÇÃO
                    # ==================================================
                    #
                    # OBJ pode possuir:
                    #
                    # - triângulos
                    # - quadrados
                    # - polígonos grandes
                    #
                    # Porém OpenGL moderno renderiza
                    # principalmente triângulos.
                    #
                    # Então precisamos converter:
                    #
                    # quad:
                    #
                    # 0 1 2 3
                    #
                    # em:
                    #
                    # triângulo 1:
                    # 0 1 2
                    #
                    # triângulo 2:
                    # 0 2 3
                    #
                    # Esse processo chama-se:
                    #
                    # triangulação
                    # ==================================================

                    for i in range(1, len(face) - 1):


                        # ==================================================
                        # MONTA TRIÂNGULO
                        # ==================================================
                        #
                        # primeiro vértice fixo
                        # formando "leque"
                        # ==================================================

                        faces.append(face[0])

                        faces.append(face[i])

                        faces.append(face[i + 1])


        # ==================================================
        # BUFFER FINAL OPENGL
        # ==================================================
        #
        # Agora iremos montar um único buffer
        # contendo:
        #
        # x y z u v
        #
        # para cada vértice.
        #
        # Esse buffer será enviado para GPU.
        # ==================================================

        buffer = []


        # ==================================================
        # PERCORRE FACES TRIANGULADAS
        # ==================================================

        for face in faces:


            # ==================================================
            # DESEMPACOTA TUPLA
            # ==================================================
            #
            # exemplo:
            #
            # (5,2)
            #
            # v_idx  = 5
            # vt_idx = 2
            # ==================================================

            v_idx, vt_idx = face


            # ==================================================
            # BUSCA VÉRTICE E UV
            # ==================================================

            vertex = vertices[v_idx]

            texcoord = textures[vt_idx]


            # ==================================================
            # ADICIONA x y z
            # ==================================================

            buffer.extend(vertex)


            # ==================================================
            # ADICIONA u v
            # ==================================================

            buffer.extend(texcoord)


        # ==================================================
        # CONVERTE PARA NUMPY
        # ==================================================
        #
        # float32:
        # padrão esperado pelo OpenGL
        # ==================================================

        buffer = np.array(buffer, dtype=np.float32)


        # ==================================================
        # QUANTIDADE DE VÉRTICES
        # ==================================================
        #
        # Cada vértice possui:
        #
        # x y z u v
        #
        # total:
        #
        # 5 floats
        #
        # então:
        #
        # total_elementos / 5
        # ==================================================

        num_vertices = len(buffer) // 5


        # ==================================================
        # RETORNO
        # ==================================================
        #
        # buffer:
        # dados finais OpenGL
        #
        # num_vertices:
        # quantidade de vértices
        # ==================================================

        return buffer, num_vertices
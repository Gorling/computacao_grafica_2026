# ==========================================================
# Trabalho Final - OpenGL Moderno
# ==========================================================
# Descrição: Cenário noturno de uma cabana na floresta.
# Utiliza os modelos (Cottage, Tree, Skull) e texturas (Grama) 
# implementados através da pipeline moderna (VAO, VBO, Shaders)
# com movimentação livre de câmara e um céu com estrelas geradas.
#
# Cumpre todos os requisitos exigidos: shaders, câmera,
# objetos 3D múltiplos, texturas, terreno e organização.
# ==========================================================

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import pyrr
from pyrr import Vector3
import ctypes
import random

# Importações dos ficheiros base do professor
from TextureLoader import load_texture
from Camera import Camera
from ObjLoaderSimple import ObjLoaderSimple

# ==========================================================
# CAMINHOS DOS ARQUIVOS (TEXTURAS E OBJETOS)
# ==========================================================

ARQUIVO_TEX_GRAMA = "texturas/grama_seca.jpg"

ARQUIVO_OBJ_COTTAGE = "OBJS/Cottage/cottage.obj"
ARQUIVO_TEX_COTTAGE = "OBJS/Cottage/House-diff.png"

ARQUIVO_OBJ_TREE = "OBJS/Tree/tree.obj"
ARQUIVO_TEX_TREE = "OBJS/Tree/tree.jpeg"

ARQUIVO_OBJ_SKULL = "OBJS/Skull/12140_Skull_v3_L2.obj"
ARQUIVO_TEX_SKULL = "OBJS/Skull/Skull.jpg"

# ==========================================================
# VARIÁVEIS GLOBAIS
# ==========================================================

WIDTH = 1024
HEIGHT = 768
Window = None

# Shaders
Shader_programm_textura = None
Shader_programm_estrelas = None

# Dados dos Modelos (VAO, Num Vértices, Textura)
vao_cottage, num_vertices_cottage, textura_cottage = None, 0, None
vao_tree, num_vertices_tree, textura_tree = None, 0, None
vao_skull, num_vertices_skull, textura_skull = None, 0, None
vao_chao, num_vertices_chao, textura_chao = None, 0, None
vao_estrelas, num_estrelas = None, 300

# Câmara
cam = Camera()
cam.camera_pos = Vector3([0.0, 2.0, -10.0]) # Posição inicial adaptada do código antigo

first_mouse = True
lastX = WIDTH / 2
lastY = HEIGHT / 2

# ==========================================================
# CALLBACKS DO SISTEMA E INPUTS
# ==========================================================

def redimensiona_callback(window, w, h):
    global WIDTH, HEIGHT
    WIDTH, HEIGHT = w
    glViewport(0, 0, WIDTH, HEIGHT)

def teclado_callback(window, key, scancode, action, mods):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)

def mouse_callback(window, xpos, ypos):
    global first_mouse, lastX, lastY
    if first_mouse:
        lastX, lastY = xpos, ypos
        first_mouse = False

    xoffset = xpos - lastX
    yoffset = lastY - ypos
    lastX, lastY = xpos, ypos

    cam.process_mouse_movement(xoffset, yoffset)

# ==========================================================
# INICIALIZAÇÃO E GERAÇÃO DE GEOMETRIAS
# ==========================================================

def inicializa_opengl():
    global Window
    if not glfw.init():
        raise RuntimeError("Erro GLFW ao iniciar")

    Window = glfw.create_window(WIDTH, HEIGHT, "Trabalho Final - Cenário Noturno (OpenGL Moderno)", None, None)
    if not Window:
        glfw.terminate()
        raise RuntimeError("Erro ao criar a Janela")

    glfw.make_context_current(Window)
    glfw.set_window_size_callback(Window, redimensiona_callback)
    glfw.set_key_callback(Window, teclado_callback)
    glfw.set_cursor_pos_callback(Window, mouse_callback)
    
    # Prende o rato no centro do ecrã para rodar a câmara estilo FPS
    glfw.set_input_mode(Window, glfw.CURSOR, glfw.CURSOR_DISABLED)
    
    glEnable(GL_DEPTH_TEST) # Teste de profundidade (3D)
    glEnable(GL_PROGRAM_POINT_SIZE) # Permite alterar o tamanho dos pontos (para as estrelas)
    glDisable(GL_CULL_FACE) # Permite ver o interior dos modelos

def carregar_objeto(arquivo_obj, arquivo_tex):
    """ Utiliza a classe do professor para carregar ficheiros OBJ e Texturas """
    buffer, num_vertices = ObjLoaderSimple.load_obj(arquivo_obj)
    buffer = buffer.astype(np.float32)

    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, buffer.nbytes, buffer, GL_STATIC_DRAW)

    stride = buffer.itemsize * 5

    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))

    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(buffer.itemsize * 3))

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    textura = glGenTextures(1)
    load_texture(arquivo_tex, textura)

    return vao, num_vertices, textura

def criar_chao(tamanho=20.0):
    """ Cria um plano largo para aplicar a textura de grama (Chão) """
    # Array [x, y, z, u, v] - Nota que o UV vai até 'tamanho' para a textura repetir
    vertices = np.array([
        -tamanho, 0.0, -tamanho,  0.0, 0.0,
         tamanho, 0.0, -tamanho,  tamanho, 0.0,
         tamanho, 0.0,  tamanho,  tamanho, tamanho,

        -tamanho, 0.0, -tamanho,  0.0, 0.0,
         tamanho, 0.0,  tamanho,  tamanho, tamanho,
        -tamanho, 0.0,  tamanho,  0.0, tamanho
    ], dtype=np.float32)

    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    stride = 5 * 4
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(3 * 4))

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    # Carrega a textura da grama usando o loader do professor
    textura = glGenTextures(1)
    load_texture(ARQUIVO_TEX_GRAMA, textura)

    return vao, 6, textura

def criar_estrelas(quantidade):
    """ Gera pontos aleatórios no alto para simular estrelas usando GL_POINTS """
    vertices = []
    for _ in range(quantidade):
        x = random.uniform(-50, 50)
        y = random.uniform(10, 40) # Estrelas sempre na parte de cima
        z = random.uniform(-50, 50)
        vertices.extend([x, y, z])

    vertices = np.array(vertices, dtype=np.float32)

    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    glEnableVertexAttribArray(0) # Apenas posições (sem textura/UV)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * 4, ctypes.c_void_p(0))

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    return vao, quantidade

# ==========================================================
# COMPILAÇÃO DOS SHADERS
# ==========================================================

def inicializa_shaders():
    global Shader_programm_textura, Shader_programm_estrelas

    # --- SHADER 1: PARA OBJETOS COM TEXTURA (COM NÉVOA) ---
    vertex_src_tex = """
        #version 400
        layout(location = 0) in vec3 in_pos;
        layout(location = 1) in vec2 in_uv;

        uniform mat4 model;
        uniform mat4 view;
        uniform mat4 projection;

        out vec2 frag_uv;
        out vec3 frag_pos; // Envia a posição 3D para o Fragment Shader

        void main() {
            frag_uv = in_uv;
            vec4 world_pos = model * vec4(in_pos, 1.0);
            frag_pos = world_pos.xyz;
            gl_Position = projection * view * world_pos;
        }
    """

    fragment_src_tex = """
        #version 400
        in vec2 frag_uv;
        in vec3 frag_pos; 

        uniform sampler2D texture1;
        uniform vec3 viewPos; // Posição atual da câmara

        out vec4 FragColor;

        void main() {
            vec4 texColor = texture(texture1, frag_uv);

            // Configurações da Névoa
            vec3 fogColor = vec3(0.02, 0.02, 0.08); // Deve ser EXATAMENTE igual ao glClearColor
            float fogDensity = 0.025; // Aumente para mais névoa, diminua para menos

            // Calcula a distância do pixel até a câmara
            float dist = distance(viewPos, frag_pos);

            // Fórmula Exponencial para uma névoa mais suave
            float fogFactor = exp(-pow(dist * fogDensity, 2.0));
            fogFactor = clamp(fogFactor, 0.0, 1.0);

            // Mistura a textura com a cor da névoa
            FragColor = mix(vec4(fogColor, 1.0), texColor, fogFactor);
        }
    """
    
    # --- SHADER 2: PARA AS ESTRELAS (Apenas cores, sem textura) ---
    vertex_src_stars = """
        #version 400
        layout(location = 0) in vec3 in_pos;
        uniform mat4 view;
        uniform mat4 projection;

        void main() {
            gl_Position = projection * view * vec4(in_pos, 1.0);
            gl_PointSize = 2.0; // Tamanho do brilho da estrela
        }
    """

    fragment_src_stars = """
        #version 400
        out vec4 FragColor;

        void main() {
            FragColor = vec4(1.0, 1.0, 1.0, 1.0); // Cor Branca
        }
    """

    # Compilar Shaders de Textura
    v_shader_tex = OpenGL.GL.shaders.compileShader(vertex_src_tex, GL_VERTEX_SHADER)
    f_shader_tex = OpenGL.GL.shaders.compileShader(fragment_src_tex, GL_FRAGMENT_SHADER)
    Shader_programm_textura = OpenGL.GL.shaders.compileProgram(v_shader_tex, f_shader_tex)

    # Compilar Shaders de Estrelas
    v_shader_stars = OpenGL.GL.shaders.compileShader(vertex_src_stars, GL_VERTEX_SHADER)
    f_shader_stars = OpenGL.GL.shaders.compileShader(fragment_src_stars, GL_FRAGMENT_SHADER)
    Shader_programm_estrelas = OpenGL.GL.shaders.compileProgram(v_shader_stars, f_shader_stars)

# ==========================================================
# LOOP DE RENDERIZAÇÃO PRINCIPAL
# ==========================================================

def render_loop():
    # Matrizes estáticas (Terreno)
    model_chao = pyrr.matrix44.create_identity()

    # Matrizes da Casa (Cottage) - Mesmas proporções e rotações do teu código antigo
    escala_cottage = pyrr.matrix44.create_from_scale(Vector3([0.85, 0.85, 0.85]))
    rotacao_cottage_y = pyrr.matrix44.create_from_y_rotation(np.radians(90))
    translacao_cottage = pyrr.matrix44.create_from_translation(Vector3([0.0, 0.0, 15.0]))
    model_cottage = pyrr.matrix44.multiply(rotacao_cottage_y, escala_cottage)
    model_cottage = pyrr.matrix44.multiply(translacao_cottage, model_cottage)

    # Matrizes base da Árvore
    escala_tree = pyrr.matrix44.create_from_scale(Vector3([1.0, 1.0, 1.0]))
    rotacao_tree_y = pyrr.matrix44.create_from_y_rotation(np.radians(90))
    posicoes_arvores = [
        [18.0, 0.0, 15.0], [-16.0, 0.0, 15.0],
        [13.0, 0.0, 15.0], [-13.0, 0.0, 15.0],
        [8.0, 0.0, 15.0],  [-8.0, 0.0, 15.0]
    ]

    # Matrizes da Caveira (Skull)
    escala_skull = pyrr.matrix44.create_from_scale(Vector3([0.025, 0.025, 0.025]))
    rotacao_skull_x = pyrr.matrix44.create_from_x_rotation(np.radians(-90))
    rotacao_skull_y = pyrr.matrix44.create_from_y_rotation(np.radians(120))
    translacao_skull = pyrr.matrix44.create_from_translation(Vector3([-4.0, -0.1, 8.0]))
    
    model_skull = pyrr.matrix44.multiply(rotacao_skull_x, escala_skull)
    model_skull = pyrr.matrix44.multiply(rotacao_skull_y, model_skull)
    model_skull = pyrr.matrix44.multiply(translacao_skull, model_skull)

    last_time = glfw.get_time()
    base_speed = 10.0

    while not glfw.window_should_close(Window):
        current_time = glfw.get_time()
        delta = current_time - last_time
        last_time = current_time
        vel = base_speed * delta

        # Input da câmara (Andar pelo cenário livremente)
        if glfw.get_key(Window, glfw.KEY_W) == glfw.PRESS:
            cam.process_keyboard("FORWARD", vel)
        if glfw.get_key(Window, glfw.KEY_S) == glfw.PRESS:
            cam.process_keyboard("BACKWARD", vel)
        if glfw.get_key(Window, glfw.KEY_A) == glfw.PRESS:
            cam.process_keyboard("LEFT", vel)
        if glfw.get_key(Window, glfw.KEY_D) == glfw.PRESS:
            cam.process_keyboard("RIGHT", vel)

        # Cor de fundo: Azul muito escuro (Céu Noturno)
        glClearColor(0.02, 0.02, 0.08, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        view = cam.get_view_matrix()
        projection = pyrr.matrix44.create_perspective_projection_matrix(45.0, WIDTH / HEIGHT, 0.1, 100.0)

        # ==================================================
        # 1. RENDERIZAÇÃO DAS ESTRELAS (SHADER SEM TEXTURA)
        # ==================================================
        glUseProgram(Shader_programm_estrelas)
        glUniformMatrix4fv(glGetUniformLocation(Shader_programm_estrelas, "view"), 1, GL_FALSE, view)
        glUniformMatrix4fv(glGetUniformLocation(Shader_programm_estrelas, "projection"), 1, GL_FALSE, projection)

        glBindVertexArray(vao_estrelas)
        glDrawArrays(GL_POINTS, 0, num_estrelas)

        # ==================================================
        # 2. RENDERIZAÇÃO DO CENÁRIO 3D (SHADER COM TEXTURA)
        # ==================================================
        glUseProgram(Shader_programm_textura)
        glUniformMatrix4fv(glGetUniformLocation(Shader_programm_textura, "view"), 1, GL_FALSE, view)
        glUniformMatrix4fv(glGetUniformLocation(Shader_programm_textura, "projection"), 1, GL_FALSE, projection)
        glUniform3f(glGetUniformLocation(Shader_programm_textura, "viewPos"), cam.camera_pos.x, cam.camera_pos.y, cam.camera_pos.z)

        # --- CHÃO (GRAMA) ---
        glUniformMatrix4fv(glGetUniformLocation(Shader_programm_textura, "model"), 1, GL_FALSE, model_chao)
        glBindVertexArray(vao_chao)
        glBindTexture(GL_TEXTURE_2D, textura_chao)
        glDrawArrays(GL_TRIANGLES, 0, num_vertices_chao)

        # --- CABANA (COTTAGE) ---
        glUniformMatrix4fv(glGetUniformLocation(Shader_programm_textura, "model"), 1, GL_FALSE, model_cottage)
        glBindVertexArray(vao_cottage)
        glBindTexture(GL_TEXTURE_2D, textura_cottage)
        glDrawArrays(GL_TRIANGLES, 0, num_vertices_cottage)

        # --- FLORESTA (ÁRVORES) ---
        glBindVertexArray(vao_tree)
        glBindTexture(GL_TEXTURE_2D, textura_tree)
        for pos in posicoes_arvores:
            trans_tree = pyrr.matrix44.create_from_translation(Vector3(pos))
            m_tree = pyrr.matrix44.multiply(rotacao_tree_y, escala_tree)
            m_tree = pyrr.matrix44.multiply(trans_tree, m_tree)
            
            glUniformMatrix4fv(glGetUniformLocation(Shader_programm_textura, "model"), 1, GL_FALSE, m_tree)
            glDrawArrays(GL_TRIANGLES, 0, num_vertices_tree)

        # --- CAVEIRA (SKULL) ---
        glUniformMatrix4fv(glGetUniformLocation(Shader_programm_textura, "model"), 1, GL_FALSE, model_skull)
        glBindVertexArray(vao_skull)
        glBindTexture(GL_TEXTURE_2D, textura_skull)
        glDrawArrays(GL_TRIANGLES, 0, num_vertices_skull)

        glfw.swap_buffers(Window)
        glfw.poll_events()

    glfw.terminate()

def main():
    global vao_cottage, num_vertices_cottage, textura_cottage
    global vao_tree, num_vertices_tree, textura_tree
    global vao_skull, num_vertices_skull, textura_skull
    global vao_chao, num_vertices_chao, textura_chao
    global vao_estrelas, num_estrelas

    inicializa_opengl()

    print("A carregar Chão e Estrelas...")
    vao_chao, num_vertices_chao, textura_chao = criar_chao(150.0)
    vao_estrelas, num_estrelas = criar_estrelas(400) # 400 estrelas no céu

    print("A carregar Cabana (Cottage)...")
    vao_cottage, num_vertices_cottage, textura_cottage = carregar_objeto(ARQUIVO_OBJ_COTTAGE, ARQUIVO_TEX_COTTAGE)
    
    print("A carregar Árvores (Tree)...")
    vao_tree, num_vertices_tree, textura_tree = carregar_objeto(ARQUIVO_OBJ_TREE, ARQUIVO_TEX_TREE)
    
    print("A carregar Caveira (Skull)...")
    vao_skull, num_vertices_skull, textura_skull = carregar_objeto(ARQUIVO_OBJ_SKULL, ARQUIVO_TEX_SKULL)

    inicializa_shaders()
    print("Renderização Iniciada. Pressiona ESC para sair.")
    render_loop()

if __name__ == "__main__":
    main()
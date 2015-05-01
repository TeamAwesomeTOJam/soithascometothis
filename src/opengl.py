import pygame
import game
import math
import numpy
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo
from OpenGL.GL import *
from OpenGL.GL.framebufferobjects import *
DO_TEXTURES = False

def createAndCompileShader(source,type):
    shader=glCreateShader(type)
    glShaderSource(shader,source)
    glCompileShader(shader)

    # get "compile status" - glCompileShader will not fail with 
    # an exception in case of syntax errors
    result=glGetShaderiv(shader,GL_COMPILE_STATUS)

    if (result!=1): # shader didn't compile
        raise Exception("Couldn't compile shader\nShader compilation Log:\n"+glGetShaderInfoLog(shader))
    return shader

class FrameBufferObject:
    def __init__(self, width = 256, height = 256):
        # Save dimensions
        self.width, self.height = width, height
        
        # Generate a framebuffer ID
        self.id = glGenFramebuffers(1)
        
        # The texture we're going to render to
        self.gl_tex_id = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, self.gl_tex_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, None)
    
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glBindTexture(GL_TEXTURE_2D, 0)

        glBindFramebuffer(GL_FRAMEBUFFER, self.id)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.gl_tex_id, 0)
        
        glDrawBuffers([GL_COLOR_ATTACHMENT0])

        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            print "Framebuffer incomplete: %s" % glCheckFramebufferStatus(GL_FRAMEBUFFER)
        
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        
        self.clear()
    
    def bind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, self.id)
        glPushAttrib(GL_VIEWPORT_BIT) # save viewport
        glViewport(0, 0, self.width, self.height)
    
    def unbind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glPopAttrib()
    
    def clear(self):
        self.bind()
        glClearColor(0.0, 0.0, 0, 0)
        glClear(GL_COLOR_BUFFER_BIT)
        self.unbind()



class GLRenderer:
    def __init__(self):
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_ALPHA | GLUT_STENCIL);
        glEnable(GL_POLYGON_SMOOTH)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)
        #glEnable(GL_ALPHA_TEST)
        glDisable(GL_DEPTH_TEST)
        self.draw_queue = []
        self.player_draw_queue = []
        vert_shader = createAndCompileShader('''

                #version 120
                uniform float aspectRatio;
                varying vec2 st;
                void main() {
                    vec4 v = gl_Vertex;
                    v.y = v.y * aspectRatio;
                gl_Position = gl_ModelViewProjectionMatrix * v;
                st = v.st;
                }
                ''',GL_VERTEX_SHADER)
        frag_shader = createAndCompileShader('''
                #version 120
                uniform vec3 color;
                void main() {
                    gl_FragColor = vec4(color,1.0);
                }
                ''',GL_FRAGMENT_SHADER)
        self.generic_shader =glCreateProgram()
        glAttachShader(self.generic_shader,vert_shader)
        glAttachShader(self.generic_shader,frag_shader)
        glLinkProgram(self.generic_shader)
        frag_shader = createAndCompileShader('''
                #version 120
                uniform vec3 color;
                varying vec2 st;
                void main() {
                    gl_FragColor = vec4(0,0,0,1);
                    gl_FragColor.rgb = color;
                }
                ''',GL_FRAGMENT_SHADER)
        self.player_shader =glCreateProgram()
        glAttachShader(self.player_shader,vert_shader)
        glAttachShader(self.player_shader,frag_shader)
        glLinkProgram(self.player_shader)


        gluOrtho2D(0,1,0,1)

        self.vbo = vbo.VBO(
                numpy.array([
                    [ 0, 1, 0],
                    [-1,-1, 0],
                    [ 1, 0, 0],
                    [ 1, 1, 0],
                    [ 0, 1, 0],
                    ]))
        self.fbox = 1280
        self.fboy = 720
        self.fbo = FrameBufferObject(self.fbox,self.fboy)
        self.fbo2 = FrameBufferObject(self.fbox,self.fboy)
        self.bg_fbo = FrameBufferObject(self.fbox,self.fboy)
        self.final_fbo = FrameBufferObject(self.fbox,self.fboy)
        self.finalRenderShader();
        self.shrinkRenderShader();
        self.resize((self.fbox,self.fboy))
        self.cleanup()
        glClearStencil(0);
        
        self.init_player()
        self.load_textures()





    def init_player(self):
        if not DO_TEXTURES: return
        self.movie = pygame.movie.Movie('/home/mtao/vid/gucci.mpg')
        self.movie_screen = pygame.Surface(self.movie.get_size()).convert()
        self.movie.set_display(self.movie_screen)
        self.movie.play()
        self.mov_tex = glGenTextures(1)


    def load_tex_from_file(self, filename):
        image      = pygame.image.load(filename)
        w,h = image.get_size()
        tex = glGenTextures(1)
        image_data = pygame.image.tostring(image, "RGBA", 1)
        glBindTexture(GL_TEXTURE_2D,tex)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S,     GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T,     GL_CLAMP_TO_EDGE)
        glTexImage2D(
                GL_TEXTURE_2D, 0,
                GL_RGBA,
                w, h, 0,
                GL_RGBA, GL_UNSIGNED_BYTE,
                image_data)
        return tex



    def load_textures(self):
        glEnable(GL_TEXTURE_2D)
        filename   = "res/images/end.png"
        self.end_tex = self.load_tex_from_file(filename)

        self.victor_texs = [0 for m in xrange(4)]
        filename   = "res/images/inbetween.png"
        self.victor_texs[0] = self.load_tex_from_file(filename)
        filename   = "res/images/1.ready.jpg"
        self.victor_texs[1] = self.load_tex_from_file(filename)
        filename   = "res/images/2.set.jpg"
        self.victor_texs[2] = self.load_tex_from_file(filename)
        filename   = "res/images/3.go.jpg"
        self.victor_texs[3] = self.load_tex_from_file(filename)



    def shrinkRenderShader(self):
        self.counter = 0
        vert_shader = createAndCompileShader('''

                #version 120
                varying vec2 st;
                void main() {
                gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
                    st = gl_MultiTexCoord0.st;
                }
                ''',GL_VERTEX_SHADER)
        frag_shader = createAndCompileShader('''
                #version 120
                uniform sampler2D tex;
                varying vec2 st;
                uniform vec2 dx;
                bool boundary(int i, int j) {
                    vec2 c = st + dx*vec2(i,j);
                    float v = texture2D(tex,c).a;
                    return v <= 0;
                }
                void main() {
                    vec4 fgcol = texture2D(tex,st);
                    if (
                        boundary(-1,-1) || boundary(-1,1)
                        || boundary(1,1) || boundary(1,-1) 
                        || boundary(0,1) || boundary(0,-1) 
                        || boundary(1,0) || boundary(-1,0) 
                        ) {
                        gl_FragColor = fgcol - vec4(0,0,0,.001);
                        gl_FragColor.rgb = vec3(1.0);
                        gl_FragColor.a = 0.001;
                    } else {
                        gl_FragColor = fgcol;
                    }
                }
                ''',GL_FRAGMENT_SHADER)
        self.shrink_shader =glCreateProgram()
        glAttachShader(self.shrink_shader,vert_shader)
        glAttachShader(self.shrink_shader,frag_shader)
        glLinkProgram(self.shrink_shader)
        dx = 1.0/self.fbox
        dy = 1.0/self.fboy
        glUseProgram(self.shrink_shader)
        loc = glGetUniformLocation(self.shrink_shader,"dx")
        glUniform2f(loc,dx,dy)
        glUseProgram(0)
    
    def finalRenderShader(self):
        vert_shader = createAndCompileShader('''

                #version 120
                varying vec2 st;
                void main() {
                gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
                    st = gl_MultiTexCoord0.st;
                    st.t = 1-st.t;
                }
                ''',GL_VERTEX_SHADER)
        frag_shader = createAndCompileShader('''
                #version 120
                uniform sampler2D bg;
                uniform sampler2D fg;
                uniform sampler2D p1tex;
                uniform sampler2D p2tex;
                uniform vec2 phase;
                varying vec2 st;

                vec4 getColor(vec4 color) {
                    vec4 ret = vec4(0,0,0,1);
                    if(color.rgb == vec3(1,0,0)) {
                        ret.rb = mod(phase+abs(vec2(cos(10*st.s),sin(10*st.t))),vec2(1,1));
                        return ret;
                        return texture2D(p1tex,vec2(st.s,1-st.t));
                    } else if (color.rgb == vec3(0,1,0)){
                        ret.bg = mod(5*st+phase.ts,vec2(1,1));
                        return ret;
                        return texture2D(p2tex,st);
                    }
                    return color;
                }
                void main() {
                    vec4 bgcol = texture2D(bg,vec2(st.s,1-st.t));
                    vec4 fgcol = texture2D(fg,st);
                    if(fgcol.a <= 0) {
                    gl_FragColor = getColor(bgcol);
                    } else {
                    gl_FragColor = getColor(fgcol);
                    }
                }
                ''',GL_FRAGMENT_SHADER)
        self.final_shader =glCreateProgram()
        glAttachShader(self.final_shader,vert_shader)
        glAttachShader(self.final_shader,frag_shader)
        glLinkProgram(self.final_shader)
        
    def createBackground(self):
        self.render_to_fbo(self.bg_fbo, self.drawBackground)
        
    def drawBackground(self):

        return
        glUseProgram(self.player_shader)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        num_split = 10
        dx = 1.0 / num_split
        color_location = glGetUniformLocation(self.player_shader, "color")
        for i in xrange(num_split):
            color = game.get_game().entity_manager.get_by_name('player' + str(2-(i%2))).color
            col = map(lambda x: x/255.0, color)

            glUniform3f(color_location, col[0],col[1],col[2])
            self.drawUVQuad(i*dx,0,dx,1)

        glUseProgram(0)



    def resize(self,tup):
        x,y = tup
        self.x = x
        self.y = y
        glViewport(0,0,x,y)
        ratio = float(x)/y
        glUseProgram(self.generic_shader)
        loc = glGetUniformLocation(self.generic_shader,"aspectRatio")
        glUniform1f(loc,ratio)
        glUseProgram(0)
        glUseProgram(self.player_shader)
        loc = glGetUniformLocation(self.player_shader,"aspectRatio")
        glUniform1f(loc,ratio)
        glUseProgram(0)

    def drawFan(self,x,y,rad,frac):
        x = float(x) / self.x
        y = float(y) / self.x
        rad = float(rad) / self.x
        glBegin(GL_TRIANGLE_FAN)
        num_div = 30
        dx = -2.0/(num_div-1) * math.pi * frac
        rot = -1*math.pi/2
        glVertex2f(x, y)
        for i in xrange(num_div):
            glVertex2f(x+math.cos(dx * i+rot) * rad, y + math.sin(dx * i+rot) * rad)
        glEnd()
    
    def drawCircle(self,x,y,rad):
        x = float(x) / self.x
        y = float(y) / self.x
        rad = float(rad) / self.x
        glBegin(GL_TRIANGLE_FAN)
        num_div = 30
        dx = 2.0/(num_div-1) * math.pi
        glVertex2f(x,y)
        for i in xrange(num_div):
            glVertex2f(x+math.cos(dx * i) * rad, y + math.sin(dx * i) * rad)
        glEnd()

    def drawRing(self,x,y,rad,rad2):
        x = float(x) / self.x
        y = float(y) / self.x
        rad = float(rad) / self.x
        rad2 = float(rad2) / self.x
        glBegin(GL_TRIANGLE_STRIP)
        num_div = 30
        dx = 2.0/(num_div-1) * math.pi
        for i in xrange(num_div):
            glVertex2f(x+math.cos(dx * i) * rad, y + math.sin(dx * i) * rad)
            glVertex2f(x+math.cos(dx * i) * rad2, y + math.sin(dx * i) * rad2)
        glEnd()
    
    def drawUVQuad(self,x,y,w,h):
        glBegin(GL_QUADS)
        glVertex2f(x,y)
        glVertex2f(x,y+h)
        glVertex2f(x+w,y+h)
        glVertex2f(x+w,y)
        glEnd()

    def drawRect(self,x,y,w,h):
        x = float(x) / self.x
        y = float(y) / self.x
        w = float(w) / self.x
        h = float(h) / self.x
        self.drawUVQuad(x,y,w,h)



    def render_ss_quad(self, layer=0):
        glBegin(GL_QUADS)

        glTexCoord2f(0, 0); glVertex3f( 0, 0,layer )
        glTexCoord2f(1, 0); glVertex3f( 1, 0,layer )
        glTexCoord2f(1, 1); glVertex3f( 1, 1,layer)
        glTexCoord2f(0, 1); glVertex3f( 0, 1,layer)

        glEnd()

    def shrink_players(self):

        glUseProgram(self.shrink_shader)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_TEXTURE_2D)


        fgloc = glGetUniformLocation(self.shrink_shader, "tex")
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.fbo.gl_tex_id)
        glUniform1i(fgloc,1)
        self.render_ss_quad()

        glDisable(GL_TEXTURE_2D)    

    def render_final_fbo(self):
        glUseProgram(self.final_shader)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if DO_TEXTURES:
            glActiveTexture(GL_TEXTURE2)
            glBindTexture(GL_TEXTURE_2D,self.mov_tex)
            loc = glGetUniformLocation(self.final_shader,"p1tex")
            glUniform1i(loc,2)


        loc = glGetUniformLocation(self.final_shader,"phase")
        glUniform2f(loc,0,self.counter/500.0)
        bgloc = glGetUniformLocation(self.final_shader, "bg")
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.bg_fbo.gl_tex_id)
        glUniform1i(bgloc,0)

        fgloc = glGetUniformLocation(self.final_shader, "fg")
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.fbo.gl_tex_id)
        glUniform1i(fgloc,1)
        self.render_ss_quad()

        glDisable(GL_TEXTURE_2D)    
        glActiveTexture(GL_TEXTURE0)
        glUseProgram(0)


    def render_tex(self,tex, layer=0):
        glViewport(0, 0, self.x,self.y)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glColor3f(1, 1, 1)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, tex)
        self.render_ss_quad(layer)

        glDisable(GL_TEXTURE_2D)    

    def render_fbo(self,fbo, layer=0):
        self.render_tex(fbo.gl_tex_id)

#     def render_players(self):
#         glClearColor(0,0,0,0)
#         #glClear(GL_COLOR_BUFFER_BIT)
#         glUseProgram(self.generic_shader)
#         #for view in self.views:
#         #    view.draw()
#         glColor3f(1,1,1);
# 
#         em = game.get_game().entity_manager
# 
# 
#         color_location = glGetUniformLocation(self.generic_shader, "color")
#         for ent in em.get_by_tag('draw_as_player'):
#             
#             col = map(lambda x: x/255.0, ent.color)
# 
#             glUniform3f(color_location, col[0],col[1],col[2])
#             self.drawCircle(ent.x,ent.y,ent.height/2.0)
#         glUseProgram(0)

    def render_to_fbo(self,fbo, func):
        fbo.bind()
        func()
        fbo.unbind()

    def render_actions(self):


        def doQueue(queue, shader):
            glUseProgram(shader)
            
            color_location = glGetUniformLocation(shader, "color")
            for item in queue:
                (a,v) = item
                if a==0:
                    color,cx,cy,r = v
                    col = map(lambda x: x/255.0, color)

                    glUniform3f(color_location, col[0],col[1],col[2])
                    self.drawCircle(cx,cy,r)
                elif a==3:
                    color,cx,cy,r,r2 = v
                    col = map(lambda x: x/255.0, color)

                    glUniform3f(color_location, col[0],col[1],col[2])
                    self.drawRing(cx,cy,r,r2)
                elif a==2:
                    color,cx,cy,r,f = v
                    col = map(lambda x: x/255.0, color)

                    glUniform3f(color_location, col[0],col[1],col[2])
                    self.drawFan(cx,cy,r,f)
                elif a==1:
                    color,x,y,w,h = v
                    col = map(lambda x: x/255.0, color)

                    glUniform3f(color_location, col[0],col[1],col[2])
                    self.drawRect(x,y,w,h)
            glUseProgram(0)
        doQueue(self.player_draw_queue,self.player_shader)
        doQueue(self.draw_queue,self.generic_shader)

        
        self.draw_queue = []
        self.player_draw_queue = []

    def appendCircle(self,color, px, py, rad):
        self.draw_queue.append( (0,(color,px,py,rad) ) )

    def appendRect(self,color, px, py, w,h):
        self.draw_queue.append( (1,(color,px,py,w,h)) )

    def appendFan(self,color, px, py, rad, frac):
        self.draw_queue.append( (2,(color,px,py,rad,frac) ) )
    def appendRing(self,color, px, py, rad, rad2):
        self.draw_queue.append( (3,(color,px,py,rad,rad2) ) )


    def appendPlayerCircle(self,color, px, py, rad):
        self.player_draw_queue.append( (0,(color,px,py,rad) ) )

    def appendPlayerRect(self,color, px, py, w,h):
        self.player_draw_queue.append( (1,(color,px,py,w,h)) )

    def appendPlayerFan(self,color, px, py, rad, frac):
        self.player_draw_queue.append( (2,(color,px,py,rad,frac) ) )
    def appendPlayerRing(self,color, px, py, rad, rad2):
        self.player_draw_queue.append( (2,(color,px,py,rad,rad2) ) )

    def cleanup(self):
        self.render_to_fbo(self.fbo,self.clean)
        self.render_to_fbo(self.bg_fbo,self.clean)
    def clean(self):
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClear(GL_COLOR_BUFFER_BIT)


    def render_victor(self,state=0,vcolor=None,ncolor = None):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.render_to_fbo(self.bg_fbo,lambda: self.render_tex(self.victor_texs[state]))

        shader = self.player_shader
        glUseProgram(shader)
        color_location = glGetUniformLocation(shader, "color")
        self.render_to_fbo(self.fbo, lambda: glClear(GL_COLOR_BUFFER_BIT))
        if vcolor is not None and state is 0:
            col = map(lambda x: x/255.0, vcolor)
            glUniform3f(color_location, col[0],col[1],col[2])
            self.render_to_fbo(self.fbo, lambda: self.drawCircle(550,300,50))
        if ncolor is not None and state is 0:
            col = map(lambda x: x/255.0, ncolor)
            glUniform3f(color_location, col[0],col[1],col[2])
            self.render_to_fbo(self.fbo, lambda: self.drawCircle(550,430,50))

        glUseProgram(0)
        self.render_final_fbo()

    def render_game_end(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.render_to_fbo(self.bg_fbo,lambda: self.render_tex(self.end_tex))
        self.render_final_fbo()
        
    def render_title(self):
        self.render_play()
#         glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#         self.render_tex(self.end_tex)

    def render_tex_crap(self):
        glUseProgram(0)


        glDisable(GL_TEXTURE_2D)


        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        w,h = self.movie_screen.get_size()
        frame = self.movie_screen
        image_data = pygame.image.tostring(frame, "RGBA", 1)
        glBindTexture(GL_TEXTURE_2D,self.mov_tex)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S,     GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T,     GL_CLAMP_TO_EDGE)
        glTexImage2D(
                GL_TEXTURE_2D, 0,
                GL_RGBA,
                w, h, 0,
                GL_RGBA, GL_UNSIGNED_BYTE,
                image_data)
        #glActiveTexture(GL_TEXTURE2)
        #self.render_tex(self.mov_tex)

    def render_layers(self):
        pass


    def render_play(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if DO_TEXTURES: self.render_tex_crap()

#         self.render_to_fbo(self.fbo,self.render_players)
        self.render_to_fbo(self.fbo,self.render_actions)
        self.render_to_fbo(self.bg_fbo,lambda: glClear(GL_COLOR_BUFFER_BIT))
        self.createBackground()



#        self.render_to_fbo(self.fbo[self.fbo_id],)
        #self.fbo_id = 1 - self.fbo_id
        #self.cleanup()
        #self.render_to_fbo(self.fbo[self.fbo_id],self.render_actions)

        def f():
            glColor4f(1,1,1,.01)
            self.render_ss_quad()
        #self.render_to_fbo(self.fbo,f)
        self.counter = self.counter + 1
#         if self.counter % 50 == 0:
#             self.render_to_fbo(self.fbo2, self.shrink_players)
#             self.fbo,self.fbo2 = self.fbo2,self.fbo
#             self.counter = 0
        self.render_final_fbo()
        glUseProgram(0)

        #glColor3f(1,1,1);
        #glBegin(GL_TRIANGLES);
        #glVertex2f(0,0);
        #glVertex2f(1,0);
        #glVertex2f(0,1);
        #glEnd();

#         size = self.movie_screen.get_size()
#         frame = self.movie_screen.get_buffer().raw
#         glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,size[0],size[1],0,GL_RGBA,GL_UNSIGNED_INT_8_8_8_8,frame)
            

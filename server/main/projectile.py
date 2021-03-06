import numpy as np

class Projectile():
    def __init__(self,server, pid, x, y, vx, vy):
        self.server=server
        self.pid=pid
        self.kind='Projectile'
        self.x=x
        self.y=y
        self.vx=vx
        self.vy=vy
        self.tick=0
        self.event='None'
        self.r=5
        
    def look_for_collider(self):
        for ent in self.server.entity_manager.entities:
            if self.server.entity_manager.entities[ent].kind=='Collider':
                collision=self.server.entity_manager.entities[ent].get_collision(self.x,self.y,self.r)
                if collision:
                    return True
                    
    def get_data(self, pid):
        data=':'.join([
                '%2d' % int(self.server.entity_manager.kind_from_to[self.kind]),
                '%6d' % int(1000*self.x),
                '%6d' % int(1000*self.y),
                '%6d' % int(100*self.vx),
                '%6d' % int(100*self.vy)
            ])
        return data
        
    def update(self):
        self.tick+=1
        self.x+=self.vx
        self.y+=self.vy
        for pid in self.server.entity_manager.entities:
            if self.server.entity_manager.entities[pid].kind=='Character':
                dx=self.x-self.server.entity_manager.entities[pid].x
                dy=self.y-self.server.entity_manager.entities[pid].y
                drsq=dx*dx+dy*dy
                drvar=self.r+self.server.entity_manager.entities[pid].r
                if drsq < drvar*drvar:
                    self.server.entity_manager.entities[pid].health-=15+np.random.rand()*5
                    if self.server.entity_manager.entities[pid].health <= 0:
                        self.server.entity_manager.event_manager.register_event('fx_destroy_character',
                            ['%6d' % int(1000*(self.server.entity_manager.entities[pid].x)),
                             '%6d' % int(1000*(self.server.entity_manager.entities[pid].y))
                            ]
                        )
                        self.server.entity_manager.event_manager.register_event('hide_character',
                            ['%d' % pid]
                        )
                        self.server.entity_manager.event_manager.register_event('show_character',
                            ['%d' % pid], 1
                        )
                        self.server.entity_manager.entities[pid].x=(np.random.rand()-0.5)*450
                        self.server.entity_manager.entities[pid].y=(np.random.rand()-0.5)*450
                        self.server.entity_manager.entities[pid].health=50
                    self.server.entity_manager.event_manager.register_event('fx_projectile_hit_character',['%6d' % int(1000*(self.x-self.vx)), '%6d' % int(1000*(self.y-self.vy))])
                    self.remove=True

        if self.look_for_collider():
            self.server.entity_manager.event_manager.register_event('fx_projectile_hit',['%6d' % int(1000*(self.x-self.vx)), '%6d' % int(1000*(self.y-self.vy))])
            self.remove=True
        
        if self.tick > 300:
            self.remove=True

def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.create_overworld(self.current_level,self.new_max_level)
        if keys[pygame.K_ESCAPE]:
            self.create_overworld(self.current_level,0)
def display_pause_screen(app, screen, pause_tick, resume_button, quit_button):

    app.pygame.mouse.set_visible(True)
    screen.blit(background_surf, (0, 0))
    if pause_tick:
        resume_button.red_tick = 10
        quit_button.red_tick = 10

    wave_change_timer  += tick_time
    song_start_t  += tick_time

    s1 = resume_button.tick(screen, mouse_pos, click_single_tick, glitch)
    quit_button.tick(screen, mouse_pos, click_single_tick, glitch, arg=app)

    scroll_bar_volume.tick(screen, mouse_pos, clicked, click_single_tick, arg = globals())
    scroll_bar_music.tick(screen, mouse_pos, clicked, click_single_tick)

    app.volume = round(scroll_bar_volume.value)
    app.music = round(scroll_bar_music.value)

    pressed = app.pygame.key.get_pressed()
    if (pressed[app.pygame.K_ESCAPE] or s1) and not pause_tick:
        menu_click2.play()
        pause = False
        pause_tick = True
        glitch.glitch_tick = 5
        app.pygame.mouse.set_visible(False)
        click_single_tick = False
        app.pygame.mixer.music.unpause()

    
    elif not pressed[app.pygame.K_ESCAPE]:
        pause_tick = False

    if not multiplayer:

        for event in app.pygame.event.get():
            if event.type == app.pygame.QUIT:
                sys.exit()

        glitch.tick()
        app.pygame.display.update()

        continue
    else:
        block_movement = True
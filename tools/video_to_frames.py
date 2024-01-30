import pygame
from moviepy.editor import VideoFileClip

def getFrames(video, size):
    video_clip = VideoFileClip(video)
    frames_iterated = video_clip.iter_frames()

    frames = [pygame.image.fromstring(frame.tobytes(), size, "RGB") for frame in video_clip.iter_frames()]
    video_clip.close()
    pygame.display.set_caption("OVRDOZE")
    return frames


if __name__ == "__main__":
    print("kulli")
    pygame.init()
    width, height = 854, 480
    screen = pygame.display.set_mode((width, height))

    video_frames = getFrames("C:/Users/Reset/Documents/GitHub/OVRDOZE/anim_compressed/intro1/video.mp4", size = [854,480])
    fps = 60
    clock = pygame.time.Clock()

    running = True
    frame_index = 0

    while running and frame_index < len(video_frames):
        screen.blit(video_frames[frame_index], (0, 0))
        pygame.display.flip()
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        frame_index += 1

    pygame.quit()
# Breakout
This is a port of classic breakout game written by JoeyDeVries to ModernGL.

The original project is:
https://learnopengl.com/In-Practice/2D-Game/Breakout

Some optimizations are made:
1. Move model-view matrix operation from application to shader, that will reduce CPU usage drastically.
2. Instanced rendering
3. Use Array Texture to avoid frequent texture switching
4. Combine multiple draw calls into one
5. Use space partitioning to increase performance of clash detection

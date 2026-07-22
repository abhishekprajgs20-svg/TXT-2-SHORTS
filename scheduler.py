import os

class SlideScheduler:
    def __init__(self, renderer):
        self.renderer = renderer

    def schedule_all(self, q, idx, temp_dir):
        slides = []

        # Queue up hook slides
        hook_img = self.renderer.render_hook(idx)
        hook_path = os.path.join(temp_dir, "slide_00.png")
        hook_img.save(hook_path)
        slides.append((hook_path, 3.0))

        # Render quiz question
        q_img = self.renderer.render_question(q, idx)
        q_path = os.path.join(temp_dir, "slide_01.png")
        q_img.save(q_path)
        slides.append((q_path, 4.0))

        # Render 10 timer slides (10 to 1)
        for sec in range(10, 0, -1):
            t_img = self.renderer.render_timer(q, idx, sec_val=sec)
            t_path = os.path.join(temp_dir, f"slide_timer_{sec:02d}.png")
            t_img.save(t_path)
            slides.append((t_path, 1.0))

        # Render answer slide
        a_img = self.renderer.render_answer(q, idx)
        a_path = os.path.join(temp_dir, "slide_answer.png")
        a_img.save(a_path)
        slides.append((a_path, 3.0))

        # Render explanation slides (each chunk)
        explanation_chunks = q.get("explanationChunks", [])
        for chunk_idx, chunk in enumerate(explanation_chunks):
            exp_img = self.renderer.render_explanation(chunk, idx)
            exp_path = os.path.join(temp_dir, f"slide_explanation_{chunk_idx:02d}.png")
            exp_img.save(exp_path)
            slides.append((exp_path, 4.0))

        # Render ending slide
        end_img = self.renderer.render_ending(idx)
        end_path = os.path.join(temp_dir, "slide_ending.png")
        end_img.save(end_path)
        slides.append((end_path, 3.0))

        return slides
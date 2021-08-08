import os

from django.shortcuts import render
from django.urls import reverse
from django.views.generic import FormView, CreateView, DetailView

from apps.color_band_training.prediction_models import predict_all
from apps.training.forms import TrainTestingCreateForm
from apps.training.models import TrainTesting
from apps.testing.image_process.strip_detect import detect_strip, locate_strip_points, pick_colors
from core.constants import Chemistry


class TrainStripUploadView(CreateView):
    template_name = 'training/train_stripe_upload.html'
    form_class = TrainTestingCreateForm
    model = TrainTesting

    def form_valid(self, form):
        self.object = form.save()
        self.process_training_image(self.object)
        return super().form_valid(form)

    @classmethod
    def process_training_image(self, training):
        if not training.original_image:
            return
        origin_img_path = training.original_image.path
        folder_path = os.path.dirname(origin_img_path)
        full_filename = os.path.basename(origin_img_path)  # with ext
        filename, ext = os.path.splitext(full_filename)
        cropped_img_path = os.path.join(folder_path, f'{filename}_cropped{ext}')

        max_score, max_box, crop_img = detect_strip(origin_img_path)

        # locate strip and pick color
        top_bottom_edges, color_points, wb_point = locate_strip_points(crop_img)
        colors = pick_colors(crop_img, color_points, top_bottom_edges, wb_point,
                             cropped_img_path)
        training.strip_crop = cropped_img_path
        training.set_crop_coordinate(max_box)
        # TH TC FC PH TA CA
        colors_dict = {
            'th': colors[0],
            'tc': colors[1],
            'fc': colors[2],
            'ph': colors[3],
            'ta': colors[4],
            'ca': colors[5],
        }

        predicts = predict_all(colors_dict)
        training.th_predict = predicts['th']
        training.fc_predict = predicts['th']
        training.tc_predict = predicts['tc']
        training.ph_predict = predicts['ph']
        training.ta_predict = predicts['ta']
        training.ca_predict = predicts['ca']
        training.save()
        return max_box

    def get_success_url(self):
        return reverse('train_stripe_detail', args=[self.object.id])


class TrainStripDetailView(DetailView):
    template_name = 'training/train_stripe_detail.html'
    model = TrainTesting

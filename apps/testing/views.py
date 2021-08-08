import os
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import FormView, CreateView, DetailView

from apps.color_band_training.prediction_models import predict_all
from apps.testing.forms import TestingCreateForm
from apps.testing.image_process.strip_detect import detect_strip, locate_strip_points, pick_colors
from apps.testing.models import Testing


class StripUploadView(CreateView):
    template_name = 'testing/stripe_upload.html'
    form_class = TestingCreateForm
    model = Testing

    def form_valid(self, form):
        self.object = form.save()
        self.process_testing_image(self.object)
        return super().form_valid(form)

    @classmethod
    def process_testing_image(self, testing):
        if not testing.original_image:
            return
        origin_img_path = testing.original_image.path
        folder_path = os.path.dirname(origin_img_path)
        full_filename = os.path.basename(origin_img_path)  # with ext
        filename, ext = os.path.splitext(full_filename)
        cropped_img_path = os.path.join(folder_path, f'{filename}_cropped{ext}')

        max_score, max_box, crop_img = detect_strip(origin_img_path, cropped_img_path)
        # locate strip and pick color
        top_bottom_edges, color_points, wb_point = locate_strip_points(crop_img)
        colors = pick_colors(crop_img, color_points, top_bottom_edges, wb_point,
                             cropped_img_path)
        testing.strip_crop = cropped_img_path
        testing.set_crop_coordinate(max_box)
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
        testing.th_value = predicts['th']
        testing.fc_value = predicts['th']
        testing.tc_value = predicts['tc']
        testing.ph_value = predicts['ph']
        testing.ta_value = predicts['ta']
        testing.ca_value = predicts['ca']
        testing.save()
        return max_box


class StripDetailView(DetailView):
    template_name = 'testing/stripe_detail.html'
    model = Testing

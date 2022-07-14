from . import BaseTestSpecFormView
from .. import services
from .. import forms

class TestSpecSummaryView(BaseTestSpecFormView):
    template_name = 'test_creator/test-spec-summary-page.html'
    form_class = forms.TestSpecSummaryForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data('summary', **kwargs)
        pages = services.get_page_list()
        num_questions = services.get_num_questions()

        context['num_pages'] = len(pages)
        context['num_versions'] = services.get_num_versions()
        context['num_questions'] = num_questions
        context['id_page'] = services.get_id_page_number()
        context['dnm_pages'] = ', '.join(str(i) for i in services.get_dnm_page_numbers())
        context['total_marks'] = services.get_total_marks()

        context['questions'] = []
        for i in range(num_questions):
            question = {}

            # TODO: question get is 1-indexed??
            question['pages'] = ', '.join(str(i) for i in services.get_question_pages(i+1))
            question['label'] = services.get_question_label(i+1)
            question['mark'] = services.get_question_marks(i+1)
            question['shuffle'] = services.get_question_fix_or_shuffle(i+1)
            context['questions'].append(question)
        return context

    def form_valid(self, form):
        
        """
        Things to does is check:

        Is there a long name and a short name?

        Are there test versions, num_to_produce, and a reference PDF?

        Is there an ID page?

        Are there questions?

        Do all the questions have pages attached?

        Do all the questions have the relevant fields?

        Are all the pages selected by something?
        """

        return super().form_valid(form)
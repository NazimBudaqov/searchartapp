from . import *

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class ImportView(APIView):
    def get(self,request):
        if request.method == 'POST':
            self.post(request)
        else:
            return render(request, 'import.html')

    def post(self,request):
        csv_file = request.FILES['file']
        csv_data = pd.read_csv(csv_file)
        print(csv_data)

        s_post = SectSubsectImportViewClass()
        s_post.post(csv_data)
        print('sectors, subsectors are imported')

        ind_count_post = IndicatorCountryImportView()
        ind_count_post.post(csv_data)
        print('indicator, countries are imported')
        
        main_post = MainDataImportViewSet()
        main_post.post(csv_data)
        print("Import complete!")
        
        # processed_rows += len(csv_data)
        # return render(request, 'import_success.html')
        
        return HttpResponse("Upload Completed!",status=200)

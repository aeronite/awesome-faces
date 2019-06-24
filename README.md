# awesome-faces
Discover awesome stuff about faces

The following environment variables are required for the azure api:<br>
- AZURE_SECRET_KEY
- AZURE_BASE_URL

Swagger Documentation here:
http://127.0.0.1:5000/

Sample usage:<br>
`curl -X POST "http://127.0.0.1:5000/faces/most_common" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"image_ids\": [ \"https://cdn.vox-cdn.com/thumbor/xAE0WGKPl8GVm2Mb8O9BUGpj5Q0=/0x0:640x427/1200x800/filters:focal(269x163:371x265)/cdn.vox-cdn.com/uploads/chorus_image/image/64080864/billgatestock.0.jpg\",\"https://fortunedotcom.files.wordpress.com/2019/02/gettyimages-1059443162-e1551207728649.jpg\",\"https://www.incimages.com/uploaded_files/image/970x450/getty_946971482_2000135218188439628_377598.jpg\",\"https://image.cnbcfm.com/api/v1/image/105462230-1537459776496gettyimages-1036093728.jpeg?v=1551363210&w=1400&h=950\" ,\"https://www.biography.com/.image/ar_1:1%2Cc_fill%2Ccs_srgb%2Cg_face%2Cq_auto:good%2Cw_300/MTQ4ODQ1NDk4NjI1Njk3NDU5/jeff-bezos-starts-amazon.jpg\" ,\"https://image.cnbcfm.com/api/v1/image/100496736-steve-jobs-march-2011-getty.jpg?v=1513863842&w=1400&h=950\" ]}"`
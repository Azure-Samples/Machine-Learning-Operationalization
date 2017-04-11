namespace CameraAppDemo
{
    using System;
    using System.Collections.Generic;
    using Android.App;
    using Android.Content;
    using Android.Content.PM;
    using Android.Graphics;
    using Android.OS;
    using Android.Provider;
    using Android.Widget;
    using Java.IO;
    using Environment = Android.OS.Environment;
    using Uri = Android.Net.Uri;
    using System.IO;

    public static class App
    {
        public static Java.IO.File _file;
        public static Java.IO.File _dir;
        public static Bitmap bitmap;
    }

    [Activity(Label = "Camera App Demo", MainLauncher = true)]
    public class MainActivity : Activity
    {
       
        private ImageView _imageView;

        protected override void OnActivityResult(int requestCode, Result resultCode, Intent data)
        {
            base.OnActivityResult(requestCode, resultCode, data);

            // Make it available in the gallery

            Intent mediaScanIntent = new Intent(Intent.ActionMediaScannerScanFile);
            Uri contentUri = Uri.FromFile(App._file);
            mediaScanIntent.SetData(contentUri);
            SendBroadcast(mediaScanIntent);

            // Display in ImageView. We will resize the bitmap to fit the display
            // Loading the full sized image will consume to much memory 
            // and cause the application to crash.

            int height = Resources.DisplayMetrics.HeightPixels;
            int width = _imageView.Height ;
            App.bitmap = App._file.Path.LoadAndResizeBitmap (width, height);
            if (App.bitmap != null) {
                _imageView.SetImageBitmap (App.bitmap);
                //App.bitmap = null;
            }

            // Dispose of the Java side bitmap.
            GC.Collect();
        }

        private async void classifyImage()
        {
            if (App.bitmap != null)
            {
                // Resize the bitmap so that it is small enough to upload to the web service 
                Bitmap bitmap = App.bitmap;
                Bitmap bitmapScaled = Bitmap.CreateScaledBitmap(bitmap, 360, 262, true);
                MemoryStream stream = new MemoryStream();
                bitmapScaled.Compress(Bitmap.CompressFormat.Jpeg, 100, stream);

                // Convert it to base64 string
                byte[] bitmapArrayImage = stream.ToArray();
                string bitmapArrayImageStr = Convert.ToBase64String(bitmapArrayImage);

                // Construct the json request body. Note that the quotes surrounding the 
                // base64 data must be escaped.
                string jsonRequest = "{ \"input\":\"[\\\"" + bitmapArrayImageStr + "\\\"]\" }";

                // Send the request
                string json = await FetchAsync.CallWebService("POST",
                                "http://<your host address>:<your service port>/score", jsonRequest);

                // Once the call returns with data, display it.
                if (json != null)
                {
                    TextView tv = FindViewById<TextView>(Resource.Id.resultsText);
                    tv.Text = json;
                }
            }
            else
            {
                TextView tv = FindViewById<TextView>(Resource.Id.resultsText);
                tv.Text = "No image to classify.";
            }
        }

        protected override void OnCreate(Bundle bundle)
        {
            base.OnCreate(bundle);
            SetContentView(Resource.Layout.Main);

            if (IsThereAnAppToTakePictures())
            {
                CreateDirectoryForPictures();

                Button button = FindViewById<Button>(Resource.Id.myButton);
                _imageView = FindViewById<ImageView>(Resource.Id.imageView1);
                button.Click += TakeAPicture;
                Button button2 = FindViewById<Button>(Resource.Id.classifyImageButton);
                button2.Click += delegate { classifyImage(); };
            }

        }

        private void CreateDirectoryForPictures()
        {
            App._dir = new Java.IO.File(
                Environment.GetExternalStoragePublicDirectory(
                    Environment.DirectoryPictures), "CameraAppDemo");
            if (!App._dir.Exists())
            {
                App._dir.Mkdirs();
            }
        }

        private bool IsThereAnAppToTakePictures()
        {
            Intent intent = new Intent(MediaStore.ActionImageCapture);
            IList<ResolveInfo> availableActivities = 
                PackageManager.QueryIntentActivities(intent, PackageInfoFlags.MatchDefaultOnly);
            return availableActivities != null && availableActivities.Count > 0;
        }

        private void TakeAPicture(object sender, EventArgs eventArgs)
        {
            Intent intent = new Intent(MediaStore.ActionImageCapture);
            App._file = new Java.IO.File(App._dir, String.Format("myPhoto_{0}.jpg", Guid.NewGuid()));
            intent.PutExtra(MediaStore.ExtraOutput, Uri.FromFile(App._file));
            StartActivityForResult(intent, 0);
        }
    }
}

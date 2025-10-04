using System.Drawing;
using System.Drawing.Drawing2D;
using System.Drawing.Imaging;
using System.Runtime.Versioning;

[SupportedOSPlatform("windows")]
class CaptchaGenerator
{
    private readonly int width;
    private readonly int height;
    private readonly FontFamily familyName;
    private readonly Random random = new();


    private static Rectangle ScaleRectCenter(Rectangle rect, float scaleFactorX, float scaleFactorY)
    {
        int newWidth = (int)(rect.Width * scaleFactorX);
        int newHeight = (int)(rect.Height * scaleFactorY);

        int newX = rect.X - (newWidth - rect.Width) / 2;
        int newY = rect.Y - (newHeight - rect.Height) / 2;

        return new Rectangle(newX, newY, newWidth, newHeight);
    }


    public CaptchaGenerator(int width, int height, string fontFamily)
    {
        this.width = width;
        this.height = height;
        this.familyName = new FontFamily(fontFamily);
    }

    public Bitmap GenerateImage(String text)
    {
        Bitmap bitmap = new(width, height, PixelFormat.Format32bppArgb);

        using (Graphics g = Graphics.FromImage(bitmap))
        {
            g.SmoothingMode = SmoothingMode.AntiAlias;
            Rectangle rect = new(0, 0, width, height);
            // Rectangle rectBigger = new(0, 0, (int)(width * 1.5), (int)(height * 1.5));

            using (HatchBrush hatchBrush = new(HatchStyle.SmallConfetti, Color.LightGray, Color.White))
            {
                g.FillRectangle(hatchBrush, rect);
            }

            float v = 3F;
            PointF[] points = {
                new(random.Next(rect.Width) / v, random.Next(rect.Height) / v),
                new(rect.Width - random.Next(rect.Width) / v, random.Next(rect.Height) / v),
                new(random.Next(rect.Width) / v, rect.Height - random.Next(rect.Height) / v),
                new(rect.Width - random.Next(rect.Width) / v, rect.Height - random.Next(rect.Height) / v)
            };

            // g.DrawPolygon(Pens.Red, points);

            Font font = new(familyName, rect.Height, FontStyle.Regular);

            // Font font2 = new(familyName, 10, FontStyle.Regular);
            // g.DrawString("Signature", font2, Brushes.Black, new PointF(0,0));

            StringFormat format = new()
            {
                Alignment = StringAlignment.Center,
                LineAlignment = StringAlignment.Center
            };

            SizeF textSize = g.MeasureString(text, font);
            float scaleX = rect.Width / textSize.Width;
            float scaleY = rect.Height / textSize.Height;
            float scale = Math.Min(scaleX, scaleY);

            GraphicsPath path = new();
            path.AddString(text, font.FontFamily, (int)font.Style, font.Size * scale, rect, format);
            path.Warp(points, ScaleRectCenter(rect, 0.5F, 0.5F));
            // path.Warp(points, rect);

            using (HatchBrush hatchBrush = new(HatchStyle.LargeConfetti, Color.LightGray, Color.DarkGray))
            {
                g.FillPath(hatchBrush, path);
            }


            int m = Math.Max(rect.Width, rect.Height);
            using (HatchBrush hatchBrush = new(HatchStyle.LargeConfetti, Color.LightGray, Color.DarkGray))
            {
                for (int i = 0; i < (int)(rect.Width * rect.Height / 40F); i++)
                {
                    int x = random.Next(rect.Width);
                    int y = random.Next(rect.Height);
                    int w = random.Next(m / 50);
                    int h = random.Next(m / 50);
                    g.FillEllipse(hatchBrush, x, y, w, h);
                }
            }

            font.Dispose();
        }

        return bitmap;
    }
}

[SupportedOSPlatform("windows")]
class Program
{
    static void Main(string[] args)
    {
        CaptchaGenerator captcha = new(160, 40, "Arial");
        Random r = new();
        for (int pass = 0; pass <= 3; pass++)
        {
            for (int i = 0; i < 10000; i++)
            {
                string randomCode = r.Next(0, 9999).ToString("0000");
                Bitmap image = captcha.GenerateImage(randomCode);
                string filePath = Path.Combine(Directory.GetCurrentDirectory(), "captchas", $"{randomCode}.{pass}.jpg");
                image.Save(filePath, ImageFormat.Jpeg);
            }
        }
    }
}

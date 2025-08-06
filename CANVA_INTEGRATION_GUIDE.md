# Canva Certificate Integration Guide

## Overview
This guide explains how the Ek Thaal platform integrates with your Canva-designed certificate template to create personalized donation certificates.

## How It Works

### 1. Template Integration
- **Canva Template**: Your `certificate.png` file serves as the base template
- **Dynamic Text Overlay**: Python's Pillow library adds donor names and certificate numbers
- **Custom Font**: Pinyon Script font for elegant donor names
- **Custom Color**: #a67b26 (golden brown) for donor names

### 2. Technical Implementation

#### Font Setup
```bash
# Font is automatically downloaded to static/fonts/PinyonScript-Regular.ttf
# The system will use this font for donor names
```

#### Image Processing
```python
# Load Canva template
template_img = PILImage.open('static/certificate.png')

# Add donor name with Pinyon Script font
font = ImageFont.truetype('static/fonts/PinyonScript-Regular.ttf', 48)
donor_color = (166, 123, 38)  # #a67b26 in RGB
draw.text((x, y), donor_name, font=font, fill=donor_color)
```

### 3. Certificate Features

#### What Gets Added to Your Template
- **Donor Name**: In Pinyon Script font, color #a67b26
- **Certificate Number**: Format EK-YYYY-XXXX
- **Positioning**: Centered on the certificate
- **Output**: High-quality PNG file

#### Customization Options

##### Font Size
```python
# Change font size (currently 48px)
font = ImageFont.truetype(font_path, 48)  # Adjust this number
```

##### Text Position
```python
# Adjust Y position (currently center - 50)
y = img_height // 2 - 50  # Adjust this offset
```

##### Color
```python
# Change donor name color (currently #a67b26)
donor_color = (166, 123, 38)  # RGB values
```

### 4. File Structure
```
ek-thal/
├── static/
│   ├── certificate.png          # Your Canva template
│   └── fonts/
│       └── PinyonScript-Regular.ttf  # Custom font
└── app/
    └── views.py                # Certificate generation logic
```

## Customization Guide

### Changing the Font
1. Download your preferred font (TTF format)
2. Place it in `static/fonts/`
3. Update the font path in `views.py`:
```python
font_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'YourFont.ttf')
```

### Adjusting Text Position
The certificate uses center positioning. To adjust:

```python
# Horizontal centering (automatic)
x = (img_width - text_width) // 2

# Vertical position (adjust these values)
y = img_height // 2 - 50  # Move up/down
cert_y = y + text_height + 30  # Certificate number position
```

### Changing Colors
```python
# Donor name color
donor_color = (166, 123, 38)  # #a67b26

# Certificate number color
cert_color = (100, 100, 100)  # Gray
```

### Adding More Text Elements
```python
# Add additional text
additional_text = "Additional Information"
text_bbox = draw.textbbox((0, 0), additional_text, font=font)
text_width = text_bbox[2] - text_bbox[0]
x = (img_width - text_width) // 2
y = y + 100  # Position below existing text
draw.text((x, y), additional_text, font=font, fill=color)
```

## Best Practices for Canva Templates

### 1. Template Design
- **High Resolution**: Use at least 2000px width for print quality
- **PNG Format**: Export as PNG for best quality
- **Transparent Areas**: Leave space for text overlay
- **Consistent Branding**: Match your platform's color scheme

### 2. Text Placement
- **Center Alignment**: Design with centered text in mind
- **Adequate Spacing**: Leave room for dynamic text
- **Readable Background**: Ensure text will be visible

### 3. File Management
- **Version Control**: Keep backup of original Canva file
- **Naming Convention**: Use descriptive filenames
- **Multiple Templates**: Create variations for different occasions

## Testing Your Integration

### 1. Local Testing
```bash
# Start the server
python manage.py runserver

# Create a test donation
# Visit the thank you page
# Click "Download Certificate"
```

### 2. Verification Checklist
- [ ] Certificate downloads as PNG
- [ ] Donor name appears in correct font
- [ ] Text color matches #a67b26
- [ ] Certificate number is visible
- [ ] Image quality is high
- [ ] Text positioning looks good

### 3. Troubleshooting

#### Font Not Loading
```python
# Check font path
print(f"Font path: {font_path}")
print(f"Font exists: {os.path.exists(font_path)}")
```

#### Template Not Found
```python
# Check template path
template_path = os.path.join(settings.BASE_DIR, 'static', 'certificate.png')
print(f"Template exists: {os.path.exists(template_path)}")
```

#### Text Positioning Issues
- Adjust the Y position values
- Check image dimensions
- Verify text bounding box calculations

## Advanced Customization

### 1. Multiple Certificate Designs
```python
# Add template selection
template_variants = {
    'standard': 'certificate.png',
    'premium': 'certificate_premium.png',
    'seasonal': 'certificate_christmas.png'
}
```

### 2. Dynamic Sizing
```python
# Adjust font size based on name length
name_length = len(donor_name)
if name_length > 20:
    font_size = 36
elif name_length > 15:
    font_size = 42
else:
    font_size = 48
```

### 3. Additional Elements
```python
# Add donation details
details_text = f"Donated {food_listing.quantity}kg of {food_listing.title}"
# Position and draw additional text
```

## Production Deployment

### 1. Font Licensing
- Ensure Pinyon Script font is licensed for web use
- Consider purchasing commercial font licenses
- Document font usage in your terms

### 2. Performance Optimization
- Cache generated certificates
- Optimize image processing
- Monitor server resources

### 3. Quality Assurance
- Test with various name lengths
- Verify print quality
- Check mobile compatibility

## Support and Maintenance

### Regular Tasks
- [ ] Update font files as needed
- [ ] Refresh certificate templates
- [ ] Monitor certificate generation logs
- [ ] Backup template files

### Monitoring
- Track certificate download rates
- Monitor generation errors
- Collect user feedback
- Analyze popular certificate designs

## Future Enhancements

### Potential Improvements
1. **Multiple Templates**: Different designs for different donation types
2. **QR Codes**: Add QR codes for verification
3. **Digital Signatures**: Add digital signatures
4. **Email Integration**: Send certificates via email
5. **Social Sharing**: Add social media sharing buttons
6. **Analytics**: Track certificate usage and impact

### Integration Ideas
1. **Canva API**: Direct integration with Canva's API
2. **Template Marketplace**: Allow users to choose designs
3. **Custom Branding**: Let organizations customize templates
4. **Seasonal Themes**: Automatic template switching based on season

## Conclusion

The Canva integration provides a beautiful, professional certificate system that:
- ✅ Uses your custom-designed template
- ✅ Adds donor names in elegant Pinyon Script font
- ✅ Applies the exact color (#a67b26) you specified
- ✅ Generates high-quality PNG files
- ✅ Includes unique certificate numbers
- ✅ Works seamlessly with your donation flow

This creates a compelling incentive for donors and provides them with a tangible reminder of their contribution to the community. 
import os
import urllib.request
import matplotlib.pyplot as plt
import urllib.parse

DARK_NAVY = '#0A1628'
ELECTRIC_BLUE = '#00A8E8'
WHITE = '#FFFFFF'
ALERT_RED = '#E53E3E'

os.makedirs('images', exist_ok=True)

def download_pollinations(prompt, filename):
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=600&nologo=true"
    print(f"Downloading {filename}...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response, open(f"images/{filename}", 'wb') as out_file:
            out_file.write(response.read())
    except Exception as e:
        print(f"Failed to download {filename}: {e}")

# Download generated images
prompts = {
    "slide1.jpg": "modern car dealership interior dark navy aesthetic photorealistic",
    "slide2.jpg": "presentation roadmap steps infographic timeline dark aesthetic",
    "slide4.jpg": "cybersecurity incident timeline infographic dark navy blue",
    "slide5.jpg": "ransomware kill chain diagram cyber attack mitre attck",
    "slide6.jpg": "car dealership employee writing on paper manually dark lighting photorealistic",
    "slide8.jpg": "disaster recovery RTO RPO timeline comparison diagram glowing dark background",
    "slide9.jpg": "fishbone ishikawa root cause analysis diagram cybersecurity dark aesthetic",
    "slide10.jpg": "NIST cybersecurity framework wheel diagram govern identify protect detect respond recover",
    "slide11.jpg": "legal compliance gavel scale cybersecurity dark aesthetic photorealistic",
    "slide12.jpg": "balance scale glowing ethics dark background photorealistic",
    "slide13.jpg": "zero trust architecture diagram network cybersecurity dark navy",
    "slide14.jpg": "venn diagram overlapping circles glowing organizational resilience",
    "slide15.jpg": "professionals engaging in discussion meeting dark aesthetic photorealistic",
    "slide16.jpg": "Questions and answers Q&A presentation slide background glowing"
}

for filename, prompt in prompts.items():
    if not os.path.exists(f"images/{filename}"):
        download_pollinations(prompt, filename)

# Create Slide 3 Pie Chart
def create_pie_chart():
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_facecolor(DARK_NAVY)
    ax.set_facecolor(DARK_NAVY)
    
    labels = ['CDK Global', 'Reynolds & Reynolds', 'Others']
    sizes = [40, 30, 30]
    colors = [ELECTRIC_BLUE, ALERT_RED, '#4A5568']
    
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                                      startangle=90, textprops=dict(color=WHITE))
    plt.title('DMS Market Share (~15,000 Dealerships)', color=WHITE, fontsize=16, pad=20)
    plt.tight_layout()
    plt.savefig('images/slide3.png', facecolor=fig.get_facecolor(), edgecolor='none', dpi=150)
    plt.close()

# Create Slide 7 Bar Chart
def create_bar_chart():
    fig, ax = plt.subplots(figsize=(7, 5))
    fig.patch.set_facecolor(DARK_NAVY)
    ax.set_facecolor(DARK_NAVY)
    
    categories = ['IBM Avg Data Breach', 'CDK Dealer Losses']
    values = [5.13, 1000] # in millions
    colors = [ELECTRIC_BLUE, ALERT_RED]
    
    bars = ax.bar(categories, values, color=colors)
    ax.set_ylabel('Impact (Millions USD)', color=WHITE, fontsize=12)
    ax.set_title('Financial Impact Comparison', color=WHITE, fontsize=16, pad=20)
    ax.tick_params(axis='x', colors=WHITE, labelsize=12)
    ax.tick_params(axis='y', colors=WHITE)
    
    # Hide spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color(WHITE)
    ax.spines['left'].set_color(WHITE)
    
    # Add text labels on bars
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + 10, f'${yval:g}M', ha='center', va='bottom', color=WHITE, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('images/slide7.png', facecolor=fig.get_facecolor(), edgecolor='none', dpi=150)
    plt.close()

if not os.path.exists('images/slide3.png'):
    create_pie_chart()
if not os.path.exists('images/slide7.png'):
    create_bar_chart()

print("All images generated.")

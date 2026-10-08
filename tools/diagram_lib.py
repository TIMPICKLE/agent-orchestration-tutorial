"""Small dependency-free SVG drawing helpers for the tutorial figures."""
from html import escape
from pathlib import Path

PALETTE = {
 'model': ('#eaf2ff','#2856a3','模型判断'),
 'program': ('#e8f6f2','#126653','程序控制'),
 'human': ('#fff3d9','#885800','人工决定'),
 'external': ('#f1ebfa','#684699','外部状态'),
 'neutral': ('#f3f5f7','#4a5768','任务信息'),
 'risk': ('#ffefec','#a13325','风险'),
}
FONT = "'Noto Sans CJK SC','Microsoft YaHei','PingFang SC',sans-serif"
class Figure:
 def __init__(self, name, title, subtitle, height=700):
  self.name=name; self.title=title; self.subtitle=subtitle; self.h=height; self.items=[]
  self.text(32,48,title,32,bold=True)
  self.text(32,86,subtitle,24,color='#4a5768')
 def text(self,x,y,s,size=28,anchor='start',bold=False,color='#182638'):
  self.items.append(f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" font-weight="{700 if bold else 400}" fill="{color}">{escape(s)}</text>')
 def rect(self,x,y,w,h,fill='#f3f5f7',stroke='none',rx=16,dash=False):
  self.items.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="2"'+(' stroke-dasharray="7 5"' if dash else '')+'/>')
 def line(self,x1,y1,x2,y2,color='#68778a',dash=False,arrow=False):
  self.items.append(f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="{color}" stroke-width="2.5"'+(' stroke-dasharray="7 5"' if dash else '')+(' marker-end="url(#arrow)"' if arrow else '')+'/>')
 def path(self,d,color='#68778a',dash=False,arrow=True):
  self.items.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2.5" stroke-linejoin="round"'+(' stroke-dasharray="7 5"' if dash else '')+(' marker-end="url(#arrow)"' if arrow else '')+'/>')
 def dot(self,x,y,n,role='program',r=22):
  fill,color,_=PALETTE[role]
  self.items.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{color}" stroke-width="2"/>')
  self.text(x,y+9,str(n),26,anchor='middle',bold=True,color=color)
 def node(self,x,y,w,title,detail='',role='program',h=112):
  fill,color,label=PALETTE[role]
  self.rect(x,y,w,h,fill)
  self.rect(x,y,7,h,color,rx=3)
  self.text(x+20,y+(24 if h<104 else 29),label,22,color=color,bold=True)
  self.text(x+20,y+(53 if h<104 else 65),title,28,bold=True)
  if detail:self.text(x+20,y+(82 if h<104 else 96),detail,24)
 def band(self,y,title,detail='',role='neutral'):
  fill,color,_=PALETTE[role]; self.rect(32,y,576,86,fill)
  self.text(52,y+35,title,28,bold=True,color=color)
  if detail:self.text(52,y+66,detail,24)
 def arrow(self,y1,y2,label='',x=320):
  self.line(x,y1,x,y2,arrow=True)
  if label:self.text(x+18,(y1+y2)/2+8,label,24,color='#4a5768')
 def note(self,y,lines,role='neutral'):
  fill,color,_=PALETTE[role]
  self.rect(32,y,576,len(lines)*34+24,fill,rx=12)
  for i,line in enumerate(lines):self.text(50,y+35+i*34,line,24,color=color)
 def save(self,root):
  y=self.h-45
  self.line(32,y-23,608,y-23,color='#dfe5eb')
  for i,role in enumerate(['model','program','human','external']):
   _,color,label=PALETTE[role]; x=32+146*i
   self.rect(x,y-4,8,22,color,rx=3);self.text(x+16,y+14,label,22,color=color)
  description='；'.join([self.subtitle, '蓝色表示模型判断，绿色表示程序控制，黄色表示人工决定，紫色表示外部状态。各角色均有文字标签。'])
  xml=f'''<svg xmlns="http://www.w3.org/2000/svg" width="640" height="{self.h}" viewBox="0 0 640 {self.h}" role="img" aria-labelledby="title desc">
<title id="title">{escape(self.title)}</title><desc id="desc">{escape(description)}</desc>
<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L8,4 L0,8" fill="#68778a"/></marker></defs>
<rect width="640" height="{self.h}" fill="#ffffff"/>
<g font-family="{FONT}">{''.join(self.items)}</g></svg>'''
  Path(root,self.name+'.svg').write_text(xml)

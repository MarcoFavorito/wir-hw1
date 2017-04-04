/*
 * "Generatore di indice" per miniHTML versione 2
 * (da usare insieme all'analizzatore lessicale realizzato con FLEX
 *  a partire da htm2.fl).
 *
 * Sequenza di comandi per generare il parser:
 *
 *     flex htm2.fl
 *     bison -d htm2.y
 *     PER DOS/WINDOWS: gcc lexyy.c htm2_tab.c -lfl -o mini2
 *     PER LINUX/UNIX: gcc lex.yy.c htm2.tab.c -lfl -o mini2
 *
 * Richiamare il parser tramite il comando:
 *
 *     mini2 < nomefileinput
 *
 * oppure ridirigendo l'output su un file:
 *
 *     mini2 < nomefileinput > nomefileoutput
 */

%{
#include<string.h>
#include<stdlib.h>

int contah1 = 0;
int contah2 = 0;
int contah3 = 0;
%}

%union {
  char stringa[800];
  int numero;
}


/*** Dichiarazione di tutti i token terminali riconosciuti da flex  ***/

%token <numero> Shtml Ehtml Shead Ehead Sbody Ebody Stitle Etitle Sol Eol Sul Eul  Sb Eb Si Ei Sfont Efont Scenter Ecenter Hr Br Sp Smeta Emeta Sanch Eanch Acontent Aname Ahref Asize Ahttpequiv Aface Awidth Equal Endtag Sli Eli Sem Eem Scode Ecode Sdd Edd String Integer Atext Alink Aalink Avlink Abgcolor Sh1 Eh1 Sh2 Eh2 Sh3 Eh3 Sh4 Eh4 Sh5 Eh5 Sh6 Eh6 

%token <stringa> Text

%type <stringa> block_text lista_text_content text_content a_tag code_tag em_tag b_tag i_tag font_tag dd_tag heading h1_tag h2_tag h3_tag 
%type <numero> 

%start html_document

%%
html_document : Shtml html_content Ehtml {} ;

html_content : head_tag body_tag {} ;

head_tag : Shead lista_head_content Ehead {} ;

lista_head_content : lista_head_content head_content | {} ;

head_content : meta_tag {} {} | title_tag {} ;

meta_tag : Smeta lista_attr_meta Endtag {} ;

lista_attr_meta : lista_attr_meta attr_meta {} | {} ;

attr_meta : Acontent Equal String {} | Aname Equal String {} |
            Ahttpequiv Equal String {} ;

title_tag : Stitle Text Etitle {} ;
 
body_tag : Sbody lista_body_attr Endtag lista_body_content Ebody {} ;

lista_body_attr : lista_body_attr body_attr {} | {} ;

body_attr: Atext Equal String {} | Alink Equal String {} | Abgcolor Equal String {} |
           Avlink Equal String {} | Aalink Equal String {} ;

lista_body_content : lista_body_content body_content {} | {} ;

body_content : hr_tag {} | block {} | heading {printf("%s\n",$1);} | text_content {} {} ;
 
hr_tag : Hr Endtag {} | Hr Awidth Equal String Endtag {} ;

block : block_content lista_block_content {} ;

lista_block_content : lista_block_content block_content {} | {} ;

block_content : ol_tag {} | ul_tag {} | center_tag {} ;

ol_tag : Sol lista_li_tag Eol {} ;

ul_tag : Sul lista_li_tag Eul {} ;

lista_li_tag : lista_li_tag li_tag {} | {} ;

li_tag : Sli lista_flow_content Eli {} ;

lista_flow_content : lista_flow_content flow_content {} | {} ;

flow_content : block {} | block_text {} ;

center_tag : Scenter lista_body_content Ecenter {} ;

heading : h1_tag | h2_tag | h3_tag | h4_tag {} | h5_tag {} | h6_tag {}  ;

h1_tag : Sh1 block_text Eh1    
   {contah2=0; contah3=0; contah1++;sprintf($$,"%d) %s",contah1,$2);} ;

h2_tag : Sh2 block_text Eh2    
   {contah3=0; contah2++; sprintf($$,"%d.%d) %s",contah1,contah2,$2);} ;

h3_tag : Sh3 block_text Eh3  
   {contah3++; sprintf($$,"%d.%d.%d) %s",contah1,contah2,contah3,$2);} ;

h4_tag : Sh4 block_text Eh4 {} ;

h5_tag : Sh5 block_text Eh5 {} ;

h6_tag : Sh6 block_text Eh6 {} ;

block_text : lista_text_content { sprintf($$,"%s",$1);} ;

lista_text_content : 
   lista_text_content text_content  {sprintf($$,"%s%s", $1,$2);} 
   | {sprintf($$,"");} ;

text_content : Text {sprintf($$,"%s",$1);} | 
               Br {sprintf($$,"");} | 
               Sp {sprintf($$,"");} | 
               a_tag {sprintf($$,"%s",$1);} | 
               code_tag {sprintf($$,"%s",$1);} | 
               em_tag {sprintf($$,"%s",$1);}| 
               b_tag {sprintf($$,"%s",$1);} | 
               i_tag {sprintf($$,"%s",$1);} | 
               font_tag {sprintf($$,"%s",$1);} | 
               dd_tag {sprintf($$,"%s",$1);} ;

a_tag : 
  Sanch Ahref Equal String Endtag block_text Eanch {sprintf($$,"%s",$6);} |
  Sanch Aname Equal String Endtag block_text Eanch {sprintf($$,"%s",$6);} ;

code_tag : Scode block_text Ecode {sprintf($$,"%s",$2);} ;

em_tag : Sem block_text Eem {sprintf($$,"%s",$2);} ;

b_tag : Sb block_text Eb {sprintf($$,"%s",$2);} ;

i_tag : Si block_text Ei {sprintf($$,"%s",$2);} ;

font_tag : 
  Sfont Asize Equal Integer Endtag block_text Efont {sprintf($$,"%s",$6);} |
  Sfont Asize Equal Integer Aface Equal String Endtag block_text Efont 
                          {sprintf($$,"%s",$9);} ; 

dd_tag : Sdd block_text Edd {sprintf($$,"%s",$2);} ;

%%

yyerror (s)  /* Called by yyparse on error */
     char *s;
	{
      printf ("%s\n", s);
    
}

main ()
{ 
 yyparse (); 
}






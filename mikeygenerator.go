// Copyright (C) 2025 Murilo Gomes Julio
// SPDX-License-Identifier: GPL-2.0-only

// Site: https://mugomes.github.io

package main

import (
	"crypto/md5"
	"crypto/sha1"
	"crypto/sha256"
	"crypto/sha512"
	"fmt"
	"image/color"
	"math/rand"
	"net/url"
	"strings"

	"github.com/mugomes/mgnumericentry"
	"github.com/mugomes/mgsmartflow"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/theme"
	"fyne.io/fyne/v2/widget"
)

const VERSION_APP string = "6.1.0"

type myDarkTheme struct{}

func (m myDarkTheme) Color(name fyne.ThemeColorName, variant fyne.ThemeVariant) color.Color {
	// A lógica para forçar o modo escuro é retornar cores escuras.
	// O Fyne usa estas constantes internamente:
	switch name {
	case theme.ColorNameBackground:
		return color.RGBA{28, 28, 28, 255} // Fundo preto
	case theme.ColorNameForeground:
		return color.White // Texto branco
	// Adicione outros casos conforme a necessidade (InputBackground, Primary, etc.)
	default:
		// Retorna o tema escuro padrão para as outras cores (se existirem)
		// Aqui estamos apenas definindo as cores principais para garantir o Dark Mode
		return theme.DefaultTheme().Color(name, theme.VariantDark)
	}
}

// 3. Implemente os outros métodos necessários da interface fyne.Theme (usando o tema padrão)
func (m myDarkTheme) Font(s fyne.TextStyle) fyne.Resource {
	return theme.DefaultTheme().Font(s)
}

func (m myDarkTheme) Icon(n fyne.ThemeIconName) fyne.Resource {
	return theme.DefaultTheme().Icon(n)
}

func (m myDarkTheme) Size(n fyne.ThemeSizeName) float32 {
	if n == theme.SizeNameText {
		return 16
	}
	return theme.DefaultTheme().Size(n)
}

func generateKey(maiuscula bool, minuscula bool, numeros bool, caracteresespeciais bool, tamanhosegmento int, tamanhochave int) string {
	var retorno, caracteres string
	if maiuscula {
		caracteres = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	}
	if minuscula {
		caracteres += "abcdefghijklmnopqrstuvwxyz"
	}
	if numeros {
		caracteres += "1234567890"
	}
	if caracteresespeciais {
		caracteres += "!@#$%*"
	}

	if caracteres == "" {
		caracteres = "abcdefghijklmnopqrstuvwxyz"
	}

	var sTamanho (int) = len(caracteres)

	var a (int) = 0
	var n (int) = 0

	var sRand int

	for a <= tamanhosegmento {
		n = 0
		for n <= tamanhochave {
			sRand = rand.Intn(sTamanho) + 1
			retorno += string(caracteres[sRand-1])
			n++
			if n == tamanhochave {
				break
			}
		}
		retorno += string('-')
		a++
		if a == tamanhosegmento {
			break
		}
	}

	// retorno[:len(retorno)-1]
	return strings.TrimRight(retorno, "-")
}

func generateHash(tipo string, valor string) string {
	var sHash string

	if tipo == "" {
		sHash = fmt.Sprintf("%x", md5.Sum([]byte(valor)))
	} else if tipo == "MD5" {
		sHash = fmt.Sprintf("%x", md5.Sum([]byte(valor)))
	} else if tipo == "SHA1" {
		sHash = fmt.Sprintf("%x", sha1.Sum([]byte(valor)))
	} else if tipo == "SHA256" {
		sHash = fmt.Sprintf("%x", sha256.Sum256([]byte(valor)))
	} else if tipo == "SHA512" {
		sHash = fmt.Sprintf("%x", sha512.Sum512([]byte(valor)))
	}

	return sHash
}

func main() {
	app := app.NewWithID("br.com.mugomes.mikeygenerator")
	app.Settings().SetTheme(&myDarkTheme{})
	window := app.NewWindow("MiKeyGenerator")
	window.SetFixedSize(true)
	window.CenterOnScreen()
	window.Resize(fyne.NewSize(500, 479))

		var txtChave *widget.Entry
	var txtHash *widget.Entry

	mnuEditar := fyne.NewMenu("Editar",
		fyne.NewMenuItem("Copiar", func() {
			app.Clipboard().SetContent(strings.Join([]string{txtChave.Text, txtHash.Text}, " "))
		}),
	)

	mnuAbout := fyne.NewMenu("Sobre",
		fyne.NewMenuItem("Verificar Atualização", func() {
			url, _ := url.Parse("https://www.mugomes.com.br/p/mikeygenerator.html")
			app.OpenURL(url)
		}),
		fyne.NewMenuItemSeparator(),
		fyne.NewMenuItem("Apoie MiKeyGenerator", func() {
			url, _ := url.Parse("https://www.mugomes.com.br/p/apoie.html")
			app.OpenURL(url)
		}),
		fyne.NewMenuItemSeparator(),
		fyne.NewMenuItem("Sobre MiKeyGenerator", func() {
			showAbout(app)
		}),
	)

	window.SetMainMenu(fyne.NewMainMenu(mnuEditar,mnuAbout))
	
	chkOptions := widget.NewCheckGroup([]string{
		"Letras Minúsculas",
		"Números",
		"Caracteres Especiais",
		"Letras Maiúsculas"}, func(s []string) {})
	chkOptions.Horizontal = false

	flow := mgsmartflow.New()
	lblTipoHash := widget.NewLabel("Tipo de Hash")
	lblTipoHash.TextStyle = fyne.TextStyle{Bold: true}
	cboTipoHash := widget.NewSelect([]string{"MD5", "SHA1", "SHA256", "SHA512"}, nil)
	cboTipoHash.PlaceHolder = "MD5"

	lblTamanho := widget.NewLabel("Tamanho")
	lblTamanho.TextStyle = fyne.TextStyle{Bold: true}

	lblTamanhoSegmento := widget.NewLabel("Segmento")
	txtTamanhoSegmento, rTamanhoSegmento := mgnumericentry.NewMGNumericEntryWithButtons(1, 100, 5)

	lblTamanhoChave := widget.NewLabel("Chave")
	txtTamanhoChave, rTamanhoChave := mgnumericentry.NewMGNumericEntryWithButtons(1, 100, 5)

	lblBox := widget.NewLabel("Opções")
	lblBox.TextStyle = fyne.TextStyle{Bold: true}
	chkBox := widget.NewCheckGroup(
		[]string{
			"Letras Maiúsculas",
			"Letras Minúsculas",
			"Números",
			"Caracteres Especiais",
		},
		nil,
	)
	chkBox.Horizontal = false
	flow.AddColumn(
		container.NewVBox(lblBox, chkBox),
		container.NewVBox(
			lblTipoHash, cboTipoHash,
			lblTamanho,
			container.NewHBox(
				container.NewVBox(lblTamanhoSegmento, txtTamanhoSegmento),
				container.NewVBox(lblTamanhoChave, txtTamanhoChave),
			),
		),
	)

	lblSeparator1 := widget.NewLabel("")
	flow.AddRow(lblSeparator1)

	btnGerar := widget.NewButton("Gerar", func() {
		sOptions := chkBox.Selected

		var sMaiuscula (bool) = false
		var sMinuscula (bool) = false
		var sNumeros (bool) = false
		var sCaracteresEspeciais (bool) = false
		for _, item := range sOptions {
			if item == "Letras Maiúsculas" {
				sMaiuscula = true
			} else if item == "Letras Minúsculas" {
				sMinuscula = true
			} else if item == "Números" {
				sNumeros = true
			} else if item == "Caracteres Especiais" {
				sCaracteresEspeciais = true
			}
		}
		txtChave.Text = generateKey(sMaiuscula, sMinuscula, sNumeros, sCaracteresEspeciais, rTamanhoSegmento.GetValue(), rTamanhoChave.GetValue())
		txtChave.Refresh()

		txtHash.Text = generateHash(cboTipoHash.Selected, txtChave.Text)
		txtHash.Refresh()

	})

	flow.AddRow(btnGerar)
	flow.SetResize(btnGerar, fyne.NewSize(150, 50))
	flow.SetMove(btnGerar, fyne.NewPos(window.Canvas().Size().Width/3.1, 0))
	flow.SetGap(btnGerar, fyne.NewPos(0, 17))

	lblChave := widget.NewLabel("Chave")
	lblChave.TextStyle = fyne.TextStyle{Bold: true}
	txtChave = widget.NewEntry()

	lblHash := widget.NewLabel("Hash")
	lblHash.TextStyle = fyne.TextStyle{Bold: true}
	txtHash = widget.NewEntry()

	flow.AddColumn(
		container.NewVBox(lblChave, txtChave),
		container.NewVBox(lblHash, txtHash),
	)

	window.SetContent(flow.Container)
	window.ShowAndRun()

}

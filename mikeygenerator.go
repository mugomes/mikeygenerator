// Copyright (C) 2025-2026 Murilo Gomes Julio
// SPDX-License-Identifier: GPL-2.0-only

// Site: https://mugomes.github.io

package main

import (
	"math/rand"
	"net/url"
	"strings"

	"github.com/mugomes/mgnumericentry"
	"github.com/mugomes/mgsmartflow"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/widget"
)

const VERSION_APP string = "1.1.0"

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

	return strings.TrimRight(retorno, "-")
}

func main() {
	sIcon := fyne.NewStaticResource("mikeygenerator.png", resourceAppIconPngData)

	app := app.NewWithID("br.com.mugomes.mikeygenerator")
	app.Settings().SetTheme(&myDarkTheme{})
	app.SetIcon(sIcon)

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
			url, _ := url.Parse("https://github.com/mugomes/mikeygenerator/releases")
			app.OpenURL(url)
		}),
		fyne.NewMenuItemSeparator(),
		fyne.NewMenuItem("Apoie MiKeyGenerator", func() {
			url, _ := url.Parse("https://mugomes.github.io/apoie.html")
			app.OpenURL(url)
		}),
		fyne.NewMenuItemSeparator(),
		fyne.NewMenuItem("Sobre MiKeyGenerator", func() {
			showAbout(app)
		}),
	)

	window.SetMainMenu(fyne.NewMainMenu(mnuEditar, mnuAbout))

	chkOptions := widget.NewCheckGroup([]string{
		"Letras Minúsculas",
		"Números",
		"Caracteres Especiais",
		"Letras Maiúsculas"}, func(s []string) {})
	chkOptions.Horizontal = false

	flow := mgsmartflow.New()
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
	})

	flow.AddRow(btnGerar)
	flow.Resize(btnGerar, 150, 50)
	flow.Move(btnGerar, window.Canvas().Size().Width/3.1, 0)
	flow.Gap(btnGerar, 0, 17)

	lblChave := widget.NewLabel("Chave")
	lblChave.TextStyle = fyne.TextStyle{Bold: true}
	txtChave = widget.NewEntry()

	flow.AddRow(lblChave)
	flow.AddRow(txtChave)

	window.SetContent(flow.Container)
	window.ShowAndRun()
}

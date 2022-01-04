"""
Author: Michael Utt

Notes:
    Use external files
        > ImplantReports
            > reports
                > lastFirst.json (look at other extensions)
                > lastFirst.pdf (a viewable file if wanted?)
            > implants.txt (maybe a folder depending on what is needed or .json)
            > properties.txt (.json?)
            > README.txt (.txt is more universal)
            >
    properties.txt
        Savepath
        LastDoctor
        AllDoctors[]
        Theme
        Color
        anesthetics[]
        tolerances[]
        prescriptions[]
        firstTime[] = false (tips to make the software clearer on first use)


    Settings menu so all the customization options are not overwhelming
        Doctor Name
        Save path (can I open an external window?)
        Various Colors
        Contact info
    First time start up menu if no preexisting properties exist
        Doctor Name:
        Save Location: C:\Program Files\ImplantReports
        Note: further customization available in settings
    <HomePage>
        Create a new implant report
            <CreateReport>
                Patient:
                    Last:   First:   Chart #:
                Surgeon: <default> or allow a new doctor to be added
                Date: <get computer time> or leave blank
                Uncover: Blank
                Restore: Blank

                [Add x-ray]

                Implant Type:
                <implant type selector>#<tooth #>
                <healing cap size?>#<tooth #>

                Restorative Part to Order:

                Report:

                Anesthestic: <options> [new anesthestic]
                Patient Tolerance: (<options> [new tolerance]) or blank
                Rx: <options> [new prescription]

                [Save]

        View implant reports
            <ViewReports>
                Search: <by name or # or doctor or date(eh)>
                Order By: <Last name or # or date added>
                Reports:
                [Last name | First name | Doctor      | Date     ]
                 Utt         Michael      David Engen   4/23/2021
            <EditReport>
                Similar to create
            <DeleteReport>
                Double check
        Add a new implant
            <CreateImplant>
                Will be easy once reports are inplace. Need more info on details.
        View implants (may merge with create implant)
            <ReadImplants>
                Search: <name>
                Implants:
                [implant name]
                [implant name]
            <EditImplant>
            <DeleteImplant>
                Double Check



    When saving a file make a backup with the previous
        How many backups? Never delete? Delete after successful open?

    Things to keep in check:
        Forward and backwards on all pages
            Do a double check on backs when on create pages
        Exit works from all places
    On save display a text bubble displaying the full path of the saved file





Time worked:
+30 hours
+16 hours
+51 hours as of 8/5
+21 - 12/10
+20 - 12/31

"""



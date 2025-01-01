from datetime import date
import streamlit as st
from services.library_service import LibraryService
from ui.components import UIComponents
import pandas as pd
import plotly.express as px

class Pages:
    def __init__(self):
        self.library_service = LibraryService()
        self.components = UIComponents()

    def render_login_page(self):
        st.title("📚 Kelana Pustaka - Masuk")
        with st.container():
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                login, register = st.columns(2)
                if login.button("Masuk", use_container_width=True, key="go_login"):
                    if username and password:
                        try:
                            user = self.library_service.auth(username, password)
                            if user:
                                st.success(f"Berhasil Masuk! Haloo.. {username}")
                                st.session_state.logged_in = True
                                st.session_state.username = username
                                st.rerun()
                        except Exception as e:
                            st.error(str(e))
                    else:
                        st.error("Invalid username or password")
                if register.button("Daftar", use_container_width=True, key="go_register"):
                    st.session_state.current_page = "regist"
                    st.rerun()
                    
    def render_library_page(self):
        # Header
        header_container = st.container()
        with header_container:
            col1, col2 = st.columns([6,1])
            with col1:
                st.title("📚 Kelana Pustaka")
            with col2:
                st.write("")
                if st.button("Logout", key="logout_button"):
                    st.session_state.logged_in = False
                    st.session_state.current_page = ""
                    st.session_state.role = ""
                    st.rerun()

        if st.session_state.role == "admin":
            # Tabs
            tabs = st.tabs([
                "Dashboard",
                "Tambah Buku", 
                "Pinjam Buku", 
                "Kembalikan Buku", 
                "Buku yang Tersedia", 
                "Buku yang Dipinjam",
                "Hibah Buku",
                "Tambah Admin"
            ])

            self._render_dashboard_tab(tabs[0])
            self._render_add_book_tab(tabs[1])
            self._render_borrow_book_tab(tabs[2])
            self._render_return_book_tab(tabs[3])
            self._render_available_books_tab(tabs[4])
            self._render_borrowed_books_tab(tabs[5])
            self._render_grant_book_tab(tabs[6])
            self._render_add_admin_tab(tabs[7])

        if st.session_state.role == "customer":
            # Tabs
            tabs = st.tabs([
                "Pinjam Buku", 
                "Buku yang Tersedia", 
                "Buku yang Dipinjam",
                "Hibah Buku"
            ])

            self._render_borrow_book_tab(tabs[0])
            self._render_available_books_tab(tabs[1])
            self._render_borrowed_books_tab(tabs[2])
            self._render_grant_book_tab(tabs[3])

    def _render_add_book_tab(self, tab):
        with tab:
            st.header("Tambah Buku Baru")
            col1, col2 = st.columns(2)
            
            with col1:
                title = st.text_input("Judul Buku")
                author = st.text_input("Penulis")
                publisher = st.text_input("Penerbit")
            
            with col2:
                isbn = st.text_input("ISBN")
                year_of_publication = st.number_input("Tahun Terbit", min_value=1900, step=1)
                pages = st.number_input("Halaman", min_value=1, step=1)
                
            synopsis = st.text_area("Sinopsis")
                
            if st.button("Add Book"):
                if title and author and isbn and publisher and year_of_publication and pages and synopsis:
                    try:
                        book = self.library_service.add_book(title, author, isbn, publisher, year_of_publication, pages, synopsis)
                        st.success(f"Book added successfully! Title: {book.title}")
                    except Exception as e:
                        st.error(str(e))
                else:
                    st.warning("Please fill in all fields")

    def _render_grant_book_tab(self, tab):
        with tab:
            st.header("Hibah Buku")
            col1, col2 = st.columns(2)
            
            with col1:
                title = st.text_input("Judul Buku", key="hibah_book_title")
                author = st.text_input("Penulis", key="hibah_book_author")
                publisher = st.text_input("Penerbit", key="hibah_book_publisher")
            
            with col2:
                isbn = st.text_input("ISBN", key="hibah_book_isbn")
                year_of_publication = st.text_input("Tahun Terbit", key="hibah_book_year")
                pages = st.text_input("Halaman", key="hibah_book_pages")
                
            synopsis = st.text_area("Sinopsis", key="hibah_book_synopsis")

            if st.button("Grant Book"):
                if title and author and isbn and publisher and year_of_publication and pages and synopsis:
                    try:
                        book = self.library_service.grant_book(title, author, isbn, publisher, year_of_publication, pages, synopsis)
                        st.success(f"Book added successfully! Title: {book.title}")
                    except Exception as e:
                        st.error(str(e))
                else:
                    st.warning("Please fill in all fields")

    def _render_borrow_book_tab(self, tab):
        with tab:
            st.header("Pinjam Buku")
            available_books = self.library_service.get_available_books()
            books = self.library_service.get_all_books()
            
            if available_books:
                top, below = st.columns(2)

                # Corrected sorting by borrow_count in ascending order to get lowest borrow counts
                sorted_books_low = sorted(books, key=lambda x: x.count_borrow)

                # Get the bottom 10 books (lowest borrow counts)
                bottom_10_books = sorted_books_low[:10]

                # Extract the sorted titles and borrow counts
                low_titles = [book.title for book in bottom_10_books]
                low_counts = [book.count_borrow for book in bottom_10_books]

                data_low = {
                'Book Title': low_titles,
                'Borrow Count': low_counts
                }

                df_low = pd.DataFrame(data_low)
                df_low = df_low.sort_values('Borrow Count', ascending=False)
                    
                fig_low = px.bar(
                    df_low,
                    x='Borrow Count',
                    y='Book Title',
                    orientation='h',
                    color='Borrow Count',
                    color_continuous_scale='Viridis',
                )
                
                fig_low.update_layout(
                    height=400,
                    xaxis_title="Top 10 Buku yang Paling Sedikit Dipinjam",
                    yaxis_title="Judul Buku",
                )

                # Corrected sorting by borrow_count in ascending order to get lowest borrow counts
                sorted_books = sorted(books, key=lambda x: x.count_borrow, reverse=True)

                # Get the bottom 10 books (lowest borrow counts)
                top_10_books = sorted_books[:10]

                # Extract the sorted titles and borrow counts
                top_titles = [book.title for book in top_10_books]
                top_counts = [book.count_borrow for book in top_10_books]

                data_low = {
                'Book Title': top_titles,
                'Borrow Count': top_counts
                }

                df_top = pd.DataFrame(data_low)
                df_top = df_top.sort_values('Borrow Count', ascending=True)
                    
                fig_top = px.bar(
                    df_top,
                    x='Borrow Count',
                    y='Book Title',
                    orientation='h',
                    color='Borrow Count',
                    color_continuous_scale='Viridis',
                )
                
                fig_top.update_layout(
                    height=400,
                    xaxis_title="Top 10 Buku paling banyak dipinjam",
                    yaxis_title="Judul Buku",
                )
                
                top.plotly_chart(fig_top, use_container_width=True)
                below.plotly_chart(fig_low, use_container_width=True)


                self.components.render_book_table(available_books)
                selected_book = st.selectbox(
                    "Select Book to Borrow",
                    [book.title for book in available_books]
                )

                if st.session_state.role == "customer":
                    student_name = st.text_input("Student Name", value=st.session_state.username, disabled=True)
                
                if st.session_state.role == "admin":
                    student_name = st.text_input("Student Name")
                
                if st.button("Pinjam Buku"):
                    if student_name:
                        if self.library_service.borrow_book(selected_book, student_name):
                            st.success(f"Book borrowed by {student_name}")
                        else:
                            st.error("Could not Pinjam Buku")
                    else:
                        st.warning("Please enter student name")
            else:
                st.info("No books available")

    def _render_return_book_tab(self, tab):
        with tab:
            st.header("Kembalikan Buku")
            borrowed_books = self.library_service.get_borrowed_books()
            
            if borrowed_books:
                self.components.render_book_table(borrowed_books, include_borrower=True)
                selected_book_id = st.selectbox(
                    "Select Book to Return",
                    [book.book_id for book in borrowed_books],
                    format_func=lambda x: next(b.title for b in borrowed_books if b.book_id == x)
                )
                
                if st.button("Kembalikan Buku"):
                    if self.library_service.return_book(selected_book_id):
                        st.success("Book returned successfully")
                    else:
                        st.error("Could not Kembalikan Buku")
            else:
                st.info("No books currently borrowed")

    def _render_available_books_tab(self, tab):
        with tab:
            st.header("Buku yang Tersedia")
            # Book data
            available_books = self.library_service.get_available_books()
            # Corrected sorting by borrow_count
            sorted_books = sorted(available_books, key=lambda x: x.count_borrow, reverse=True)

            # Get the top 10 books
            top_10_books = sorted_books[:10]

            # Extract the sorted titles and borrow counts
            book_titles = [book.title for book in top_10_books]
            borrow_counts = [book.count_borrow for book in top_10_books]

            data = {
                'Book Title': book_titles,
                'Borrow Count': borrow_counts
            }

            df = pd.DataFrame(data)
            df = df.sort_values('Borrow Count', ascending=True)
                
            fig = px.bar(
                df,
                x='Borrow Count',
                y='Book Title',
                orientation='h',
                color='Borrow Count',
                color_continuous_scale='Viridis',
            )
            
            fig.update_layout(
                height=400,
                xaxis_title="Top 10 Buku paling banyak dipinjam",
                yaxis_title="Judul Buku",
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            self.components.render_book_table(available_books)

    def _render_borrowed_books_tab(self, tab):
        with tab:
            st.header("Buku yang Dipinjam")
            borrowed_books = self.library_service.get_borrowed_books()
            self.components.render_book_table(borrowed_books, include_borrower=True)

    def _render_dashboard_tab(self, tab):
        with tab:
            st.header("Dashboard Kelana Pustaka")
            st.success('Hello... ' + st.session_state.username, icon="👋")
            books = self.library_service.get_all_books()
            users = self.library_service.get_users()
            col1, col2 = st.columns(2)
            col1.metric("Total User", len(users))
            col2.metric("Total Buku", len(books))

            st.markdown("---")

            # st.columns(2)
            
    def _welcome_tab(self, tab):
        with tab:
            st.markdown("### Petualangan Literasi Tanpa Batas")
    
            # Compelling Welcome Message
            st.markdown("""
            Selamat datang di dunia tanpa batas Kelana Pustaka, tempat di mana setiap halaman 
            membuka pintu menuju petualangan baru. Kami hadir untuk mengubah cara Anda 
            menjelajahi dunia literasi digital Indonesia.
            
            ✨ *"Setiap buku adalah tiket menuju perjalanan pengetahuan yang tak terlupakan"*
            """)

            st.markdown("---")
            
            # Benefits Section
            st.markdown("### Mengapa Kelana Pustaka?")
            st.markdown("""
            Kami memahami bahwa setiap pembaca adalah penjelajah unik. Di Kelana Pustaka, 
            Anda akan menemukan pengalaman membaca yang berbeda:
            
            • Akses ke ribuan judul pilihan dari penulis terbaik Indonesia dan dunia\n
            • Rekomendasi personal berdasarkan minat dan preferensi Anda\n
            • Komunitas pembaca yang aktif dan inspiratif
            """)

            st.markdown("---")
            
            # Features
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("### 📖 Koleksi Tak Terbatas")
                st.write("Jelajahi ribuan buku dari berbagai genre. Dari fiksi hingga non-fiksi, klasik hingga kontemporer.")
            
            with col2:
                st.markdown("### 🔍 Pencarian Cerdas")
                st.write("Sistem rekomendasi AI yang memahami selera Anda. Temukan buku berikutnya dengan mudah.")
            
            with col3:
                st.markdown("### 👥 Komunitas Aktif")
                st.write("Bergabung dengan ribuan pembaca. Diskusi, ulasan, dan rekomendasi dari sesama pecinta buku.")
            
            st.markdown("---")

            # Coming Soon
            st.markdown("### 🚀 Segera Hadir")
            st.markdown("""
            • Book Club digital dengan diskusi mingguan\n
            • Sesi virtual meet-the-author\n
            • Sistem reward untuk pembaca aktif
            """)
            
            # Footer
            st.markdown("---")
            st.markdown("""
            © 2024 Kelana Pustaka | Membuka Cakrawala Literasi Indonesia
            
            *Bergabunglah dalam perjalanan literasi bersama ribuan pembaca lainnya*
            """)

    def render_public_page(self):
        # Header
        header_container = st.container()
        with header_container:
            col1, col2 = st.columns([6,1])
            with col1:
                st.title("📚 Kelana Pustaka - Beranda")
            with col2:
                # This column is for buttons, centered layout
                st.write("")  # Empty space to center buttons in column
                
                login, register = st.columns(2)
                if login.button("Masuk", use_container_width=True, key="go_login"):
                    st.session_state.current_page = "masuk"
                    st.rerun()
                if register.button("Daftar", use_container_width=True, key="go_register"):
                    st.session_state.current_page = "regist"
                    st.rerun()
            # with col3:
            #     st.write("")

        # Tabs
        tabs = st.tabs([
            "Beranda",
            "Buku yang Tersedia", 
            "Buku yang Dipinjam"
        ])

        self._welcome_tab(tabs[0])
        self._render_available_books_tab(tabs[1])
        self._render_borrowed_books_tab(tabs[2])

    def render_register_page(self):
        header_container = st.container()
        with header_container:
            col1, col2 = st.columns([6,1])
            with col1:
                st.title("📚 Kelana Pustaka - Daftar")
            with col2:
                st.write("")  
                if st.button("Masuk", use_container_width=True, key="go_login"):
                    st.session_state.current_page = "masuk"
                    st.rerun()
        
        # st.markdown("---")
        # st.header("Halaman Pendaftaran")

        # Data Pribadi
        st.subheader("👤 Data Pribadi")
        id_number = st.text_input("NIK", 
                                max_chars=16, 
                                placeholder="Masukkan 16 digit NIK Anda")
        
        full_name = st.text_input("Nama Lengkap",
                                placeholder="Masukkan nama lengkap Anda")
        
        # Tempat & Tanggal Lahir dalam satu baris
        birth_col1, birth_col2 = st.columns(2)
        with birth_col1:
            birthplace = st.text_input("Tempat Lahir",
                                    placeholder="Kota kelahiran")
        with birth_col2:
            min_date = date(date.today().year - 100, 1, 1)
            max_date = date.today()
            birthdate = st.date_input("Tanggal Lahir",
                                    min_value=min_date,
                                    max_value=max_date,
                                    value=date(2000, 1, 1))
        
        gender = st.selectbox("Jenis Kelamin", 
                            ["Pilih jenis kelamin", "Laki-Laki", "Perempuan"])
        
        address = st.text_area("Alamat",
                            placeholder="Masukkan alamat lengkap Anda",
                            height=100)
        
        st.markdown("---")
        
        # Data Akun
        st.subheader("🔐 Data Akun")
        
        # Username & Email dalam satu baris
        user_col1, user_col2 = st.columns(2)
        with user_col1:
            username = st.text_input("Username",
                                placeholder="Masukkan username")
        with user_col2:
            email = st.text_input("Email",
                                placeholder="contoh@email.com")
        
        # Password & Konfirmasi dalam satu baris
        pass_col1, pass_col2 = st.columns(2)
        with pass_col1:
            password = st.text_input("Kata Sandi",
                                type="password",
                                placeholder="Minimal 6 karakter")
        with pass_col2:
            confirm_password = st.text_input("Konfirmasi Kata Sandi",
                                        type="password",
                                        placeholder="Ulangi kata sandi")
        
        # Validasi password real-time
        if confirm_password:
            if password != confirm_password:
                st.error("❌ Kata Sandi tidak cocok")
            elif len(confirm_password) < 6:
                st.warning("⚠️ Kata Sandi harus lebih dari 6 karakter")
            else:
                st.success("✅ Kata Sandi cocok!")
        
        submit_button = st.button("Daftar")
        
        if submit_button:
            # Validasi form
            if not id_number:
                st.error("NIK diperlukan")
            elif len(id_number) != 16 or not id_number.isdigit():
                st.error("NIK harus terdiri dari 16 digit")
            elif not full_name:
                st.error("Nama Lengkap diperlukan")
            elif not birthplace:
                st.error("Tempat Lahir diperlukan")
            elif gender == "Pilih jenis kelamin":
                st.error("Jenis Kelamin diperlukan")
            elif not address:
                st.error("Alamat diperlukan")
            elif not username:
                st.error("Username diperlukan")
            elif not email or '@' not in email or '.' not in email:
                st.error("Silakan masukkan alamat email yang valid")
            elif not password or len(password) < 6:
                st.error("Kata Sandi harus lebih dari 6 karakter")
            elif password != confirm_password:
                st.error("Kata Sandi tidak cocok")
            else:
                try:
                    user = self.library_service.add_user_public(id_number, full_name, birthplace, birthdate, gender, address, username, email, password, "customer")
                    st.success(f"Pendaftaran berhasil! Haloo.. {user.username}")
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.role = "customer"
                    st.rerun()
                except Exception as e:
                    st.error(str(e))

    def _render_add_admin_tab(self, tab):
        with tab:
            st.header("Tambah Admin")

            # Data Pribadi
            st.subheader("👤 Data Pribadi")
            id_number = st.text_input("NIK", 
                                    max_chars=16, 
                                    placeholder="Masukkan 16 digit NIK Anda")
            
            full_name = st.text_input("Nama Lengkap",
                                    placeholder="Masukkan nama lengkap Anda")
            
            # Tempat & Tanggal Lahir dalam satu baris
            birth_col1, birth_col2 = st.columns(2)
            with birth_col1:
                birthplace = st.text_input("Tempat Lahir",
                                        placeholder="Kota kelahiran")
            with birth_col2:
                min_date = date(date.today().year - 100, 1, 1)
                max_date = date.today()
                birthdate = st.date_input("Tanggal Lahir",
                                        min_value=min_date,
                                        max_value=max_date,
                                        value=date(2000, 1, 1))
            
            gender = st.selectbox("Jenis Kelamin", 
                                ["Pilih jenis kelamin", "Laki-Laki", "Perempuan"])
            
            address = st.text_area("Alamat",
                                placeholder="Masukkan alamat lengkap Anda",
                                height=100)
            
            st.markdown("---")
            
            # Data Akun
            st.subheader("🔐 Data Akun")
            
            # Username & Email dalam satu baris
            user_col1, user_col2 = st.columns(2)
            with user_col1:
                username = st.text_input("Username",
                                    placeholder="Masukkan username")
            with user_col2:
                email = st.text_input("Email",
                                    placeholder="contoh@email.com")
            
            # Password & Konfirmasi dalam satu baris
            pass_col1, pass_col2 = st.columns(2)
            with pass_col1:
                password = st.text_input("Kata Sandi",
                                    type="password",
                                    placeholder="Minimal 6 karakter")
            with pass_col2:
                confirm_password = st.text_input("Konfirmasi Kata Sandi",
                                            type="password",
                                            placeholder="Ulangi kata sandi")
            
            # Validasi password real-time
            if confirm_password:
                if password != confirm_password:
                    st.error("❌ Kata Sandi tidak cocok")
                elif len(confirm_password) < 6:
                    st.warning("⚠️ Kata Sandi harus lebih dari 6 karakter")
                else:
                    st.success("✅ Kata Sandi cocok!")
            
            submit_button = st.button("Daftar")
            
            if submit_button:
                # Validasi form
                if not id_number:
                    st.error("NIK diperlukan")
                elif len(id_number) != 16 or not id_number.isdigit():
                    st.error("NIK harus terdiri dari 16 digit")
                elif not full_name:
                    st.error("Nama Lengkap diperlukan")
                elif not birthplace:
                    st.error("Tempat Lahir diperlukan")
                elif gender == "Pilih jenis kelamin":
                    st.error("Jenis Kelamin diperlukan")
                elif not address:
                    st.error("Alamat diperlukan")
                elif not username:
                    st.error("Username diperlukan")
                elif not email or '@' not in email or '.' not in email:
                    st.error("Silakan masukkan alamat email yang valid")
                elif not password or len(password) < 6:
                    st.error("Kata Sandi harus lebih dari 6 karakter")
                elif password != confirm_password:
                    st.error("Kata Sandi tidak cocok")
                else:
                    try:
                        user = self.library_service.add_user_public(id_number, full_name, birthplace, birthdate, gender, address, username, email, password, "admin")
                        st.success(f"Pendaftaran berhasil! Haloo.. {user.username}")
                    except Exception as e:
                        st.error(str(e))
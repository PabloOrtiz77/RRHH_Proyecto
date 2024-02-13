-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 12, 2024 at 05:56 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `astil`
--

-- --------------------------------------------------------

--
-- Table structure for table `adelantos_actualizados`
--

CREATE TABLE `adelantos_actualizados` (
  `id` int(11) NOT NULL,
  `id_adelanto` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `adelantos_actualizados`
--

INSERT INTO `adelantos_actualizados` (`id`, `id_adelanto`) VALUES
(13, 23);

-- --------------------------------------------------------

--
-- Table structure for table `asistencias`
--

CREATE TABLE `asistencias` (
  `id_asistencia` int(11) NOT NULL,
  `dia` varchar(25) NOT NULL,
  `fecha` date NOT NULL,
  `primer_turno_E` varchar(20) NOT NULL,
  `primer_turno_S` varchar(20) NOT NULL,
  `segundo_turno_E` varchar(20) NOT NULL,
  `segundo_turno_S` varchar(20) NOT NULL,
  `horas_tot_dia` varchar(20) NOT NULL,
  `id_empleado` int(11) NOT NULL,
  `id_cliente` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `asistencias`
--

INSERT INTO `asistencias` (`id_asistencia`, `dia`, `fecha`, `primer_turno_E`, `primer_turno_S`, `segundo_turno_E`, `segundo_turno_S`, `horas_tot_dia`, `id_empleado`, `id_cliente`) VALUES
(68, 'Miércoles', '2024-01-10', '07:00', '12:00', '14:00', '18:00', '0 9:0:0', 40, 20),
(69, 'Jueves', '2024-01-11', '12:00', '13:00', '14:00', '20:00', '0 7:0:0', 40, 20),
(70, 'Jueves', '2024-01-11', '12:00', '13:00', '14:00', '20:00', '0 7:0:0', 40, 20),
(71, 'Viernes', '2024-01-12', '07:00', '12:00', '14:00', '17:00', '0 8:0:0', 40, 20),
(72, 'Viernes', '2024-01-12', '07:00', '12:00', '14:00', '17:00', '0 8:0:0', 41, 20),
(73, 'Jueves', '2024-02-01', '07:00', '12:00', '14:00', '17:00', '0 8:0:0', 40, 20),
(74, 'Martes', '2024-01-30', '07:00', '12:00', '15:00', '17:00', '0 7:0:0', 41, 20),
(75, 'Lunes', '2024-02-01', '07:00', '12:00', '14:00', '17:00', '0 8:0:0', 41, 20),
(76, 'Martes', '2024-01-30', '07:00', '12:00', '14:00', '17:00', '0 8:0:0', 42, 21),
(77, 'Martes', '2024-01-30', '07:00', '12:00', '14:00', '17:00', '0 8:0:0', 43, 21),
(78, 'Viernes', '2024-02-02', '15:04', '15:04', '15:04', '15:04', '0 0:0:0', 40, 20),
(79, 'Sábado', '2024-02-02', '09:52', '09:52', '09:54', '09:55', '0 0:1:0', 40, 20),
(80, 'Domingo', '2024-02-11', '09:52', '09:53', '09:54', '09:55', '0 0:2:0', 40, 20),
(81, 'Sábado', '2024-02-11', '10:25', '11:24', '10:25', '10:25', '0 0:59:0', 40, 20),
(82, 'Sábado', '2024-03-03', '10:25', '11:24', '10:25', '10:25', '0 0:59:0', 40, 20),
(83, 'Domingo', '2024-02-11', '18:44', '19:44', '19:44', '19:44', '0 1:0:0', 40, 20),
(84, 'Domingo', '2024-03-08', '18:44', '19:44', '19:44', '19:44', '0 1:0:0', 40, 20),
(85, 'Lunes', '2024-02-12', '10:59', '10:00', '11:00', '11:00', '-1 23:1:0', 40, 20),
(86, 'Lunes', '2024-02-12', '11:00', '11:00', '11:00', '11:00', '0 0:0:0', 40, 20),
(87, 'Lunes', '2024-02-13', '11:01', '11:01', '11:01', '11:01', '0 0:0:0', 40, 20);

-- --------------------------------------------------------

--
-- Table structure for table `auditoria`
--

CREATE TABLE `auditoria` (
  `id_auditoria` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `descripcion` text NOT NULL,
  `fecha` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Dumping data for table `auditoria`
--

INSERT INTO `auditoria` (`id_auditoria`, `id_usuario`, `descripcion`, `fecha`) VALUES
(1, 0, 'El usuario maxifarma se ha registrado', '2024-02-11'),
(2, 4, 'Inicio de sesión', '2024-02-12'),
(3, 4, 'Inicio de sesión', '2024-02-12'),
(4, 4, 'Se ha actualizado el cliente Casino', '2024-02-12'),
(5, 4, 'Se ha añadido el cliente Supermercado Typasy', '2024-02-12'),
(6, 4, 'Se ha actualizado el cliente Supermercado Typasy', '2024-02-12'),
(7, 4, 'Se ha añadido el empleado Juan', '2024-02-12'),
(8, 4, 'Cierre de sesión', '2024-02-12'),
(9, 31, 'Cierre de sesión', '2024-02-12'),
(10, 31, 'Cierre de sesión', '2024-02-12'),
(11, 31, 'Cierre de sesión', '2024-02-12'),
(12, 34, 'Cierre de sesión', '2024-02-12'),
(13, 0, 'El usuario casino se ha registrado', '2024-02-12'),
(14, 37, 'Cierre de sesión', '2024-02-12'),
(15, 29, 'Inicio de sesión', '2024-02-12'),
(16, 29, 'Inicio de sesión', '2024-02-12'),
(17, 29, 'Cierre de sesión', '2024-02-12');

-- --------------------------------------------------------

--
-- Table structure for table `caja`
--

CREATE TABLE `caja` (
  `id_caja` int(11) NOT NULL,
  `monto` int(11) NOT NULL,
  `ruc_cliente` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `caja`
--

INSERT INTO `caja` (`id_caja`, `monto`, `ruc_cliente`) VALUES
(12, 15000000, '45676-4'),
(13, 0, '45676-56'),
(14, 0, '4444555-6'),
(15, 0, '5604645452'),
(19, 0, '3003031-6'),
(20, 0, '123454321');

-- --------------------------------------------------------

--
-- Table structure for table `cashadvance`
--

CREATE TABLE `cashadvance` (
  `id` int(11) NOT NULL,
  `date_advance` date NOT NULL,
  `employee_id` int(15) NOT NULL,
  `amount` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `cashadvance`
--

INSERT INTO `cashadvance` (`id`, `date_advance`, `employee_id`, `amount`) VALUES
(23, '2024-02-21', 40, 100000);

-- --------------------------------------------------------

--
-- Table structure for table `clientes`
--

CREATE TABLE `clientes` (
  `id_cliente` int(11) NOT NULL,
  `razon_social` varchar(45) NOT NULL,
  `ruc` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `contrato` varchar(150) NOT NULL,
  `telefono` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `clientes`
--

INSERT INTO `clientes` (`id_cliente`, `razon_social`, `ruc`, `email`, `contrato`, `telefono`) VALUES
(20, 'Casino', '45676-4', 'pabloantonioortiz77@gmail.com', 'ResponseSummary.pdf', '0984512535'),
(21, 'Super la paz', '45676-56', 'pudiortiz_01@hotmail.com', 'Etica_Social_1parte.pdf', '0984512535'),
(22, 'Super6', '4444555-6', 'super6@super6.com', '2020-Scrum-Guide-US.pdf', '09856065646'),
(23, 'Super Plub', '5604645452', 'super@plub.com', 'recibo_pago_Julio_enero.pdf', '098560656463'),
(27, 'Supermercado Esperanza', '3003031-6', 'esperanza@supermercado.com', 'recibo_pago_Julio_enero.pdf', '0985112345'),
(28, 'Supermercado Typasy', '123454321', 'typasy@gmail.com', 'recibo_pago_Julio_enero.pdf', '123123154142');

-- --------------------------------------------------------

--
-- Table structure for table `deductions`
--

CREATE TABLE `deductions` (
  `id` int(11) NOT NULL,
  `description` varchar(45) NOT NULL,
  `amount` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `deductions`
--

INSERT INTO `deductions` (`id`, `description`, `amount`) VALUES
(23, 'ips', 9);

-- --------------------------------------------------------

--
-- Table structure for table `empleados`
--

CREATE TABLE `empleados` (
  `idEmpleados` int(11) NOT NULL,
  `nombre_completo` varchar(45) NOT NULL,
  `apellido_completo` varchar(45) NOT NULL,
  `documento` varchar(45) NOT NULL,
  `contrato` varchar(255) NOT NULL,
  `idNacionalidad` int(11) NOT NULL,
  `idPuesto` int(11) NOT NULL,
  `idEstado` int(11) NOT NULL,
  `telefono` varchar(45) NOT NULL,
  `id_cliente` int(11) NOT NULL,
  `id_tipo_empleado` int(11) NOT NULL,
  `Fecha_de_ingreso` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `empleados`
--

INSERT INTO `empleados` (`idEmpleados`, `nombre_completo`, `apellido_completo`, `documento`, `contrato`, `idNacionalidad`, `idPuesto`, `idEstado`, `telefono`, `id_cliente`, `id_tipo_empleado`, `Fecha_de_ingreso`) VALUES
(40, 'Julio', 'Torales', '2112121', 'ResponseSummary.pdf', 10, 5, 1, '28188', 20, 3, '2021-01-21'),
(41, 'Pablo ', 'Ortiz', '7454674', 'Desafio_Return_Pablo_Ortiz.pdf', 10, 5, 1, '0984512535', 20, 4, '2019-06-21'),
(42, 'Juan', 'Guzman', '838383', 'recibo_pago_Julio_enero_4.pdf', 10, 5, 1, '09299292', 21, 3, '2016-06-20'),
(43, 'Fernando', 'Ortiz', '323232', 'recibo_pago_Pablo__febrero.pdf', 10, 5, 1, '0033232', 21, 4, '2020-06-20'),
(45, 'Marcos', 'Ferreira', '6546464', 'ScrumGlossary.pdf', 14, 7, 1, '4355136178', 21, 3, '2024-02-02'),
(47, 'Juan', 'Romero', '44444444', 'recibo_pago_Julio_enero.pdf', 10, 5, 1, '333341343', 28, 4, '2024-02-12');

-- --------------------------------------------------------

--
-- Table structure for table `estado_empleado`
--

CREATE TABLE `estado_empleado` (
  `idEstado_Empleado` int(11) NOT NULL,
  `Descripcion` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `estado_empleado`
--

INSERT INTO `estado_empleado` (`idEstado_Empleado`, `Descripcion`) VALUES
(1, 'Activo'),
(2, 'Inactivo');

-- --------------------------------------------------------

--
-- Table structure for table `faltas_mensualeros`
--

CREATE TABLE `faltas_mensualeros` (
  `id_falta` int(11) NOT NULL,
  `documento` int(11) NOT NULL,
  `fecha` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `faltas_mensualeros`
--

INSERT INTO `faltas_mensualeros` (`id_falta`, `documento`, `fecha`) VALUES
(3, 7454674, '2024-01-21');

-- --------------------------------------------------------

--
-- Table structure for table `nacionalidad`
--

CREATE TABLE `nacionalidad` (
  `idNacionalidad` int(11) NOT NULL,
  `Nacionalidad` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `nacionalidad`
--

INSERT INTO `nacionalidad` (`idNacionalidad`, `Nacionalidad`) VALUES
(10, 'Paraguaya'),
(11, 'Brasilera'),
(12, 'Chilena'),
(13, 'Argentina'),
(14, 'Ecuatoriana');

-- --------------------------------------------------------

--
-- Table structure for table `nominas_salario`
--

CREATE TABLE `nominas_salario` (
  `id_nomina` int(11) NOT NULL,
  `id_empleado` int(11) DEFAULT NULL,
  `sueldo` int(11) DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `Deducciones` int(11) NOT NULL,
  `Retiros` int(11) NOT NULL,
  `Salario_Neto` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `nominas_salario`
--

INSERT INTO `nominas_salario` (`id_nomina`, `id_empleado`, `sueldo`, `fecha`, `Deducciones`, `Retiros`, `Salario_Neto`) VALUES
(13, 40, 399477, '2024-01-10', 39947, 0, 359530),
(14, 41, 2680373, '2024-01-12', 268037, 0, 2322990),
(15, 41, 2680373, '2024-02-01', 268037, 0, 2412336),
(16, 42, 103091, '2024-01-30', 10309, 0, 92782),
(17, 43, 2680373, '2024-01-30', 268037, 0, 2412336),
(18, 40, -476581, '2024-02-02', -47658, 0, -428923),
(20, 40, -476581, '2024-02-11', -47658, 0, -428923),
(22, 40, 25557, '2024-03-03', 2555, 0, 23002),
(24, 40, 25557, '2024-03-08', 2555, 0, 23002),
(25, 40, -476581, '2024-02-12', -47658, 0, -428923),
(27, 40, -476581, '2024-02-13', -47658, 0, -428923),
(28, 41, 2500000, '2024-02-12', 250000, 0, 2250000),
(29, 43, 2500000, '2024-02-12', 250000, 0, 2250000),
(30, 47, 2500000, '2024-02-12', 250000, 0, 2250000);

-- --------------------------------------------------------

--
-- Table structure for table `puesto`
--

CREATE TABLE `puesto` (
  `idPuesto` int(11) NOT NULL,
  `Categoria` varchar(45) DEFAULT NULL,
  `jornaldiario_para_mensualeros` int(11) NOT NULL,
  `jornaldiario_para_jornaleros` int(11) NOT NULL,
  `mensual` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `puesto`
--

INSERT INTO `puesto` (`idPuesto`, `Categoria`, `jornaldiario_para_mensualeros`, `jornaldiario_para_jornaleros`, `mensual`) VALUES
(5, 'Basado en el Salario Minimo', 89346, 103091, 2680373),
(7, 'Ganadería', 62542, 72164, 1876261);

-- --------------------------------------------------------

--
-- Table structure for table `tipo_empleado`
--

CREATE TABLE `tipo_empleado` (
  `id_tipo_empleado` int(11) NOT NULL,
  `descripcion_tipo` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tipo_empleado`
--

INSERT INTO `tipo_empleado` (`id_tipo_empleado`, `descripcion_tipo`) VALUES
(3, 'Jornalero'),
(4, 'Mensualero');

-- --------------------------------------------------------

--
-- Table structure for table `tipo_usuario`
--

CREATE TABLE `tipo_usuario` (
  `id_tipo_usuario` int(11) NOT NULL,
  `Descripcion_tipo` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tipo_usuario`
--

INSERT INTO `tipo_usuario` (`id_tipo_usuario`, `Descripcion_tipo`) VALUES
(1, 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `nombre_completo` varchar(45) NOT NULL,
  `documento` varchar(45) NOT NULL,
  `usuario` varchar(45) NOT NULL,
  `contrasena` varchar(100) NOT NULL,
  `tipo_usuario` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `nombre_completo`, `documento`, `usuario`, `contrasena`, `tipo_usuario`) VALUES
(1, 'Pablo Ortiz', '7454674', 'Pablo Ortiz', 'dede', 3),
(2, 'Pablo Ortiz', '7454674', 'Pablo Ortiz', 'fcb123', 3),
(3, 'Antonio Ortiz', '333333', 'Ramon', 'sss', 2),
(4, 'admin', '12345', 'admin', 'admin123', 1),
(5, 'Walter Gonzales', '4323453', 'Walter', '21122', 2),
(6, 'Victor Arrua', '22321', 'Victor', '12345', 3),
(16, '2', '2', '22', '2', 2),
(17, 'Julio', '2122', 'JUlio', '213', 2),
(20, 'La frameña', '54555', 'piter', '12345', 2),
(21, 'La frameña', '5604645', 'MarcosFerr', '1234', 2),
(22, 'La frameña', '523423412', 'piterparker', '1234', 2),
(23, 'La frameña', '54555', 'piterprime', '1234', 2),
(24, 'La frameña', '54555', 'pitermax', '1234', 2),
(25, 'La frameña', '1231', 'primemax', '1234', 2),
(26, 'La frameña', '12312', 'maxpiter', '$2b$12$Uz07tIrFmh3gUmQviK6pI.gFt8E5mP4Sem53bHPUNrOW0jAskkdI.', 2),
(27, 'La frameña', '553131', 'pedromax', '$2b$12$S3IgHvg1lHwZbRuoumW/wegKsAbwAUWYcuLTE64zmhwY74RY8o2Ou', 3),
(28, 'PedroPaco', '56034-4', 'pedropaco', '$2b$12$CkIDyg6DDLiUrcfH/aKeuec2bqp1dovWkyTX5pMgy2LjRZDaYL.TW', 3),
(29, 'Marcos', '6546464', 'marcosferr', '$2b$12$fuJfiSquqff3B5ZgQpEqMOQuqa8i.NvPWOFoM3HtCNNsMonliJIBu', 3),
(30, 'Marcos', '6546464', 'marcosferr', '$2b$12$MblJB.BAciyrbAREC6u1T.6DC50W7EKHnE37e2uPS9N6e8BLVS3bq', 3),
(31, 'SuperSeis', '111111', 'andymax', '$2b$12$SkD9bAZp2WI8Ds3QqNe9zOFKPzZH/jiGgTab3sLqYYo69NcsvQkim', 2),
(33, 'Carrefour', '56044444', 'pedrog', '$2b$12$UmShvvB.JHrjz0zJdHTf.ek3qxxFMQEGYFGVynAAZvbYZ8F4Dp03G', 2),
(34, 'La Familia', '12313131', 'lafamiliaadmin', '$2b$12$CHeIWhORTVhhbEcR4rCLXOYD6QbDtftEEFu.pF5KJ1XLa791m8Cvu', 2),
(35, 'MaxiFarma', '333333', 'maxifarma', '$2b$12$NG2IZ1qVuUdydVdyfpL00.RlaMi9fb6BXGZAVl1pNRdtIpRIOb28y', 2),
(37, 'Casino', '45676-4', 'casino', '$2b$12$hCkrXLYEZECA9rJSnGhEhulnx9De86hLZnmpDs8qpgJZtaQPUzvaK', 2);

-- --------------------------------------------------------

--
-- Table structure for table `vacaciones`
--

CREATE TABLE `vacaciones` (
  `idVacacion` int(11) NOT NULL,
  `idEmpresa` int(11) NOT NULL,
  `fechaInicio` date NOT NULL,
  `fechaFin` date NOT NULL,
  `idEmpleado` int(11) NOT NULL,
  `estado` varchar(20) NOT NULL DEFAULT 'Pendiente'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Dumping data for table `vacaciones`
--

INSERT INTO `vacaciones` (`idVacacion`, `idEmpresa`, `fechaInicio`, `fechaFin`, `idEmpleado`, `estado`) VALUES
(4, 21, '2024-02-01', '2024-02-02', 45, 'Rechazado'),
(5, 21, '2024-02-01', '2024-02-17', 45, 'Rechazado');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `adelantos_actualizados`
--
ALTER TABLE `adelantos_actualizados`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id_adelanto` (`id_adelanto`);

--
-- Indexes for table `asistencias`
--
ALTER TABLE `asistencias`
  ADD PRIMARY KEY (`id_asistencia`),
  ADD KEY `id_empleado` (`id_empleado`,`id_cliente`),
  ADD KEY `id_cliente` (`id_cliente`);

--
-- Indexes for table `auditoria`
--
ALTER TABLE `auditoria`
  ADD PRIMARY KEY (`id_auditoria`);

--
-- Indexes for table `caja`
--
ALTER TABLE `caja`
  ADD PRIMARY KEY (`id_caja`),
  ADD KEY `id_cliente` (`ruc_cliente`),
  ADD KEY `ruc_cliente` (`ruc_cliente`);

--
-- Indexes for table `cashadvance`
--
ALTER TABLE `cashadvance`
  ADD PRIMARY KEY (`id`),
  ADD KEY `employee_id` (`employee_id`);

--
-- Indexes for table `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`id_cliente`),
  ADD KEY `ruc` (`ruc`);

--
-- Indexes for table `deductions`
--
ALTER TABLE `deductions`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `empleados`
--
ALTER TABLE `empleados`
  ADD PRIMARY KEY (`idEmpleados`),
  ADD KEY `idNacionalidad` (`idNacionalidad`),
  ADD KEY `idPuesto` (`idPuesto`),
  ADD KEY `idEstado` (`idEstado`),
  ADD KEY `id_cliente` (`id_cliente`),
  ADD KEY `id_cliente_2` (`id_cliente`);

--
-- Indexes for table `estado_empleado`
--
ALTER TABLE `estado_empleado`
  ADD PRIMARY KEY (`idEstado_Empleado`);

--
-- Indexes for table `faltas_mensualeros`
--
ALTER TABLE `faltas_mensualeros`
  ADD PRIMARY KEY (`id_falta`);

--
-- Indexes for table `nacionalidad`
--
ALTER TABLE `nacionalidad`
  ADD PRIMARY KEY (`idNacionalidad`);

--
-- Indexes for table `nominas_salario`
--
ALTER TABLE `nominas_salario`
  ADD PRIMARY KEY (`id_nomina`),
  ADD UNIQUE KEY `unique_employee_month_year` (`id_empleado`,`fecha`);

--
-- Indexes for table `puesto`
--
ALTER TABLE `puesto`
  ADD PRIMARY KEY (`idPuesto`);

--
-- Indexes for table `tipo_empleado`
--
ALTER TABLE `tipo_empleado`
  ADD PRIMARY KEY (`id_tipo_empleado`);

--
-- Indexes for table `tipo_usuario`
--
ALTER TABLE `tipo_usuario`
  ADD PRIMARY KEY (`id_tipo_usuario`);

--
-- Indexes for table `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`),
  ADD KEY `tipo_usuario` (`tipo_usuario`);

--
-- Indexes for table `vacaciones`
--
ALTER TABLE `vacaciones`
  ADD PRIMARY KEY (`idVacacion`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `adelantos_actualizados`
--
ALTER TABLE `adelantos_actualizados`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `asistencias`
--
ALTER TABLE `asistencias`
  MODIFY `id_asistencia` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=88;

--
-- AUTO_INCREMENT for table `auditoria`
--
ALTER TABLE `auditoria`
  MODIFY `id_auditoria` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `caja`
--
ALTER TABLE `caja`
  MODIFY `id_caja` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `cashadvance`
--
ALTER TABLE `cashadvance`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `clientes`
--
ALTER TABLE `clientes`
  MODIFY `id_cliente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT for table `deductions`
--
ALTER TABLE `deductions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table `empleados`
--
ALTER TABLE `empleados`
  MODIFY `idEmpleados` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=48;

--
-- AUTO_INCREMENT for table `faltas_mensualeros`
--
ALTER TABLE `faltas_mensualeros`
  MODIFY `id_falta` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `nacionalidad`
--
ALTER TABLE `nacionalidad`
  MODIFY `idNacionalidad` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `nominas_salario`
--
ALTER TABLE `nominas_salario`
  MODIFY `id_nomina` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT for table `puesto`
--
ALTER TABLE `puesto`
  MODIFY `idPuesto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `tipo_empleado`
--
ALTER TABLE `tipo_empleado`
  MODIFY `id_tipo_empleado` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=38;

--
-- AUTO_INCREMENT for table `vacaciones`
--
ALTER TABLE `vacaciones`
  MODIFY `idVacacion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `adelantos_actualizados`
--
ALTER TABLE `adelantos_actualizados`
  ADD CONSTRAINT `adelantos_actualizados_ibfk_1` FOREIGN KEY (`id_adelanto`) REFERENCES `cashadvance` (`id`);

--
-- Constraints for table `asistencias`
--
ALTER TABLE `asistencias`
  ADD CONSTRAINT `asistencias_ibfk_1` FOREIGN KEY (`id_empleado`) REFERENCES `empleados` (`idEmpleados`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `asistencias_ibfk_2` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id_cliente`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `caja`
--
ALTER TABLE `caja`
  ADD CONSTRAINT `caja_ibfk_1` FOREIGN KEY (`ruc_cliente`) REFERENCES `clientes` (`ruc`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `cashadvance`
--
ALTER TABLE `cashadvance`
  ADD CONSTRAINT `cashadvance_ibfk_1` FOREIGN KEY (`employee_id`) REFERENCES `empleados` (`idEmpleados`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `empleados`
--
ALTER TABLE `empleados`
  ADD CONSTRAINT `empleados_ibfk_3` FOREIGN KEY (`idEstado`) REFERENCES `estado_empleado` (`idEstado_Empleado`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `empleados_ibfk_4` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id_cliente`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `empleados_ibfk_6` FOREIGN KEY (`idNacionalidad`) REFERENCES `nacionalidad` (`idNacionalidad`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `tipo_usuario`
--
ALTER TABLE `tipo_usuario`
  ADD CONSTRAINT `tipo_usuario_ibfk_1` FOREIGN KEY (`id_tipo_usuario`) REFERENCES `usuarios` (`tipo_usuario`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
